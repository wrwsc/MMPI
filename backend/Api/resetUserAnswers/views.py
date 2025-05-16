from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from Dal.models import User, UserAnswer, UserTScore
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@method_decorator(csrf_exempt, name='dispatch')
class ApiResetUserAnswers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Сброс всех ответов и T-оценок пользователя",
        responses={
            200: openapi.Response("Результаты успешно сброшены"),
            404: openapi.Response("Пользователь не найден")
        }
    )
    def delete(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        user_answer = UserAnswer.objects.filter(user=user).first()

        answers_cleared = 0
        if user_answer:
            for i in range(1, 567):
                field_name = f"Вопрос {i}"
                if hasattr(user_answer, field_name):
                    setattr(user_answer, field_name, None)
            user_answer.save()
            answers_cleared = 1
        tscores_deleted, _ = UserTScore.objects.filter(user=user).delete()

        return Response(status=status.HTTP_200_OK)
