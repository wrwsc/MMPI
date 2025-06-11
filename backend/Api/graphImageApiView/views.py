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
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class GraphImageAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self, request, user_id):
        try:
            print(f"Получаем пользователя с user_id={user_id}")
            target_user = User.objects.get(user_id=user_id)
            print(f"Пользователь найден: {target_user}")
            print(f"Получаем текущего пользователя по request.user={request.user}")

            from django.core.exceptions import ObjectDoesNotExist
            try:
                current_user = User.objects.get(django_user=request.user)
            except ObjectDoesNotExist:
                return Response({"message": "Ошибка: текущий пользователь не найден"}, status=401)

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
            try:
                cached_png = redis_client.get(cache_key)
            except Exception as ex:
                print(f"Ошибка доступа к Redis: {ex}")
                cached_png = None

            if cached_png:
                graph_image = io.BytesIO(cached_png)
                graph_image.seek(0)
            else:
                graph_image = generate_graph(t_scores)
                try:
                    redis_client.set(cache_key, graph_image.getvalue(), ex=60 * 60 * 24)
                except Exception as ex:
                    print(f"Ошибка при сохранении графика в Redis: {ex}")

            response = HttpResponse(graph_image.getvalue(), content_type='image/png')
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=500)