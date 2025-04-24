from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Dal.models import UserAnswer, User
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt


class ApiDeleteUserAnswer(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Удалить ответ пользователя по ID и ID вопроса",
        operation_summary="Удалить конкретный ответ пользователя",
        parameters=[
            openapi.Parameter('user_id', openapi.IN_PATH, description="ID пользователя", type=openapi.TYPE_INTEGER),
            openapi.Parameter('question_id', openapi.IN_PATH, description="ID вопроса", type=openapi.TYPE_INTEGER),
        ],
        responses={
            204: openapi.Response('Ответ удален'),
            404: openapi.Response('Пользователь или вопрос не найден')
        }
    )
    def delete(self, request, user_id, question_id):
        if request.user.id != user_id:
            return Response({"message": "Вы не можете удалять ответы другого пользователя."},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(id=user_id)
            user_answer = UserAnswer.objects.get(user=user)
            question_field = f"Вопрос {question_id}"

            if not hasattr(user_answer, question_field):
                return Response({"message": "Ответ на данный вопрос не найден"}, status=status.HTTP_404_NOT_FOUND)

            setattr(user_answer, question_field, None)
            user_answer.save()

            return Response({"message": "Ответ удален"}, status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        except UserAnswer.DoesNotExist:
            return Response({"message": "Ответы пользователя не найдены"}, status=status.HTTP_404_NOT_FOUND)
