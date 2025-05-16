from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from Dal.models import User, UserAnswer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@method_decorator(csrf_exempt, name='dispatch')
class ApiTestStatus(APIView):
    authentication_classes = [TokenAuthentication] # для теста в swagger надо удалить это и method_decorator с csrf_exempt
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny] для теста в swagger

    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Получить количество отвеченных вопросов пользователем",
        responses={
            200: openapi.Response("Количество успешно получено"),
            404: openapi.Response("Пользователь не найден")
        }
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        user_answer = UserAnswer.objects.filter(user=user).first()
        if not user_answer:
            return Response({
                "user_id": user_id,
                "answered": 0
            }, status=status.HTTP_200_OK)

        answered = sum(
            1 for i in range(1, 567)
            if getattr(user_answer, f"Вопрос {i}", None) is not None
        )

        return Response({
            "user_id": user_id,
            "answered": answered
        }, status=status.HTTP_200_OK)
