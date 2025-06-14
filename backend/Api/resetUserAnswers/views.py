from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from Dal.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


@method_decorator(csrf_exempt, name='dispatch')
class ApiResetUserAnswers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny] для теста в swagger

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

        Token.objects.filter(user=user.django_user).delete()
        user.django_user.delete()

        return Response({"message": "Все данные пользователя удалены"}, status=status.HTTP_200_OK)
