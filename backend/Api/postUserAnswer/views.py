from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from Logic.serializatorQuery.serilizer import UserAnswerSerializer
from django.views.decorators.csrf import csrf_exempt

class ApiPostUserAnswer(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @swagger_auto_schema(
        operation_description="Ответ пользователя",
        operation_summary="Ответ на вопрос",
        request_body=UserAnswerSerializer,
        responses={
            200: openapi.Response('Ответ успешно сохранен', UserAnswerSerializer),
            400: openapi.Response('Ошибка при сохранении ответа')
        }
    )
    def post(self, request, user_id):
        if request.user.id != user_id:
            return Response({"message": "Вы не можете изменять ответы другого пользователя."},
                            status=status.HTTP_403_FORBIDDEN)
        data = request.data
        data['user'] = request.user.id
        serializer = UserAnswerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Сохранился ответ"}, status=status.HTTP_200_OK)

        return Response({"message": "Не сохранился ответ", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
