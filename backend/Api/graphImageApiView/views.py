import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponse
from Dal.models import User
from Logic.calculate.saveTScores import save_user_t_scores
from Logic.calculate.scoring import (
    has_completed_all_questions,
    calculate_raw_scores,
    apply_corrections,
    calculate_t_scores, generate_graph, get_redis_key, redis_client
)
from Dal.tables.table import M_table, delta_table
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class GraphImageAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Экспорт графика и результатов тестов для указанного пользователя",
        operation_summary="Получить результаты теста в формате PDF для пользователя",
        responses={
            200: openapi.Response('PDF файл с результатами',
                                  content={'application/pdf': openapi.Schema(type='string', format='binary')}),
            403: openapi.Response('Ошибка доступа: пользователь пытается получить данные другого пользователя'),
            404: openapi.Response('Пользователь не найден'),
        },
    )
    def get(self, request, user_id):
        try:
            target_user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=404)

        current_user = User.objects.get(django_user=request.user)
        if not request.user.is_superuser and current_user.user_id != target_user.user_id:
            return Response({"message": "Доступ запрещен"}, status=403)

        if not has_completed_all_questions(target_user):
            return Response({"message": "Не все вопросы заполнены"}, status=400)

        raw_scores = calculate_raw_scores(target_user)
        corrected_scores = apply_corrections(raw_scores)
        t_scores = calculate_t_scores(corrected_scores, M_table, delta_table, target_user.sex)

        original_t_value = request.query_params.get("original_T", None)
        if original_t_value is not None:
            try:
                original_t_value = float(original_t_value)
            except ValueError:
                return Response({"message": "Неверное значение для original_T"}, status=400)

        save_user_t_scores(target_user, t_scores, raw_scores, original_t_value)

        cache_key = get_redis_key(target_user.user_id, t_scores)
        cached_png = redis_client.get(cache_key)

        if cached_png:
            graph_image = io.BytesIO(cached_png)
            graph_image.seek(0)
        else:
            graph_image = generate_graph(t_scores)
            redis_client.set(cache_key, graph_image.getvalue(), ex=60 * 60 * 24)

        response = HttpResponse(graph_image.getvalue(), content_type='image/png')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response