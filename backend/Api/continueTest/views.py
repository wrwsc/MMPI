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
class ApiContinueTest(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        user_answer = UserAnswer.objects.filter(user=user).first()

        if not user_answer:
            return Response({
                "user_id": user_id,
                "next_question_number": 1,
                "answered_count": 0,
            }, status=status.HTTP_200_OK)

        for i in range(1, 567):
            answer = getattr(user_answer, f"Вопрос {i}", None)
            if answer is None:
                return Response({
                    "user_id": user_id,
                    "next_question_number": i,
                    "answered_count": i - 1,
                }, status=status.HTTP_200_OK)

        return Response({"user_id": user_id, "next_question_number": None, "answered_count": 566,}, status=status.HTTP_200_OK)
