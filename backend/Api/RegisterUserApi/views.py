from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from Logic.serializatorRegister.serializer import RegisterUserSerializer

class RegisterUserApi(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Регистрация нового пользователя",
        request_body=RegisterUserSerializer,
        responses={
            201: openapi.Response("Пользователь зарегистрирован"),
            400: openapi.Response("Ошибка валидации")
        }
    )
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user, token = serializer.save()
            return Response({
                "user_id": user.user_id,
                "email": user.email,
                "token": token.key,
                "message": "Регистрация успешна",
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)