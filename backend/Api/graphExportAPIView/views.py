from Dal.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Dal.tables.table import M_table, delta_table
from Logic.calculate.scoring import (
    calculate_t_scores, calculate_raw_scores,
    apply_corrections, generate_graph, generate_pdf, has_completed_all_questions
)
from rest_framework.exceptions import AuthenticationFailed
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import AuthenticationFailed
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class GraphExportAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
        print(f"Авторизованный пользователь: {request.user}")
        try:
            target_user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        current_user = User.objects.get(django_user=request.user)
        if not request.user.is_superuser and current_user.user_id != target_user.user_id:
            return Response({"message": "Вы не можете получить данные другого пользователя"}, status=status.HTTP_403_FORBIDDEN)

        if not has_completed_all_questions(target_user):
            return Response(
                {"message": "Пользователь не ответил на все вопросы"},
                status=status.HTTP_400_BAD_REQUEST
            )

        raw_scores = calculate_raw_scores(target_user)
        corrected_scores = apply_corrections(raw_scores)
        t_scores = calculate_t_scores(corrected_scores, M_table, delta_table, target_user.sex)

        graph_file = generate_graph(t_scores)
        pdf_file = generate_pdf(graph_file, target_user)

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="test_results.pdf"'
        return response
