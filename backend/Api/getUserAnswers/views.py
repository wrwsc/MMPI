from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Dal.models import UserAnswer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt

class ApiGetUserAnswers(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self, request, user_id=None):
        if request.user.id != user_id:
            return Response({"message": "Вы не можете просматривать ответы другого пользователя."},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            user_answers = UserAnswer.objects.get(user_id=user_id)

            answers_dict = {}

            for field in user_answers._meta.fields:
                if field.name.startswith("Вопрос"):
                    answers_dict[field.name] = getattr(user_answers, field.name)

            return Response(answers_dict, status=status.HTTP_200_OK)

        except UserAnswer.DoesNotExist:
            return Response({"message": "Пользователь не ответил на вопросы."}, status=status.HTTP_404_NOT_FOUND)