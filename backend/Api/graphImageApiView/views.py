import io
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
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

class GraphImageAPIView(APIView):
    permission_classes = [AllowAny]

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
            print(f"==> Получаем пользователя с user_id={user_id}")
            target_user = User.objects.get(user_id=user_id)
            print(f"target_user найден: {target_user}")

            print(f"==> Получаем текущего пользователя по request.user={request.user}")
            from django.core.exceptions import ObjectDoesNotExist
            try:
                current_user = User.objects.get(django_user=request.user)
            except ObjectDoesNotExist:
                print("Текущий пользователь не найден в Dal.User")
                return Response({"message": "Ошибка: текущий пользователь не найден"}, status=401)
            print(f"current_user найден: {current_user}")

            if not request.user.is_superuser and current_user.user_id != target_user.user_id:
                print(f"Доступ запрещен: {request.user} хочет получить данные {target_user.user_id}")
                return Response({"message": "Доступ запрещен"}, status=403)

            print("==> Проверяем, все ли вопросы заполнены")
            if not has_completed_all_questions(target_user):
                print("Не все вопросы заполнены")
                return Response({"message": "Не все вопросы заполнены"}, status=400)

            print("==> Считаем сырые баллы")
            raw_scores = calculate_raw_scores(target_user)
            print(f"raw_scores: {raw_scores}")

            print("==> Корректируем баллы")
            corrected_scores = apply_corrections(raw_scores)
            print(f"corrected_scores: {corrected_scores}")

            print("==> Считаем T-баллы")
            t_scores = calculate_t_scores(corrected_scores, M_table, delta_table, target_user.sex)
            print(f"t_scores: {t_scores}")

            original_t_value = request.query_params.get("original_T", None)
            if original_t_value is not None:
                try:
                    original_t_value = float(original_t_value)
                except ValueError:
                    print("Неверное значение для original_T")
                    return Response({"message": "Неверное значение для original_T"}, status=400)

            print("==> Сохраняем t_scores пользователя")
            save_user_t_scores(target_user, t_scores, raw_scores, original_t_value)

            cache_key = get_redis_key(target_user.user_id, t_scores)
            print(f"==> Проверяем кэш Redis: cache_key={cache_key}")
            try:
                cached_png = redis_client.get(cache_key)
            except Exception as ex:
                print(f"Ошибка доступа к Redis: {ex}")
                cached_png = None

            if cached_png:
                print("График найден в кэше Redis")
                graph_image = io.BytesIO(cached_png)
                graph_image.seek(0)
            else:
                print("==> Генерируем график")
                graph_image = generate_graph(t_scores)
                try:
                    redis_client.set(cache_key, graph_image.getvalue(), ex=60 * 60 * 24)
                    print("График сохранён в Redis")
                except Exception as ex:
                    print(f"Ошибка при сохранении графика в Redis: {ex}")

            print("==> Формируем ответ")
            response = HttpResponse(graph_image.getvalue(), content_type='image/png')
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            print("==> Успех! График отдан клиенту")
            return response

        except Exception as e:
            print("=== ОШИБКА ВЫПОЛНЕНИЯ ===")
            print(e)
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)