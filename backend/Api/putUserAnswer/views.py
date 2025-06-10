from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Dal.models import UserAnswer, User
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication


class ApiPutUserAnswer(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def put(self, request, user_id, question_id, answer):
        if request.user.id != user_id:
            print(request.user.id, '    ', user_id)
            return Response({"message": "Вы не можете изменять ответы другого пользователя."},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(id=user_id)
            
            user_answer = UserAnswer.objects.get(user=user)

            question_field = f"Вопрос {question_id}"

            if answer not in ['Да', 'Нет']:
                return Response({"message": "Ответ должен быть 'Да' или 'Нет'"}, status=status.HTTP_400_BAD_REQUEST)
            
            setattr(user_answer, question_field, answer)
            user_answer.save()

            return Response({"message": "Ответ успешно обновлен"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        except UserAnswer.DoesNotExist:
            return Response({"message": "Ответы пользователя не найдены"}, status=status.HTTP_404_NOT_FOUND)
