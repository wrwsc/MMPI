from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from Logic.serializatorQuery.serilizer import UserAnswerSerializer

class ApiPostUserAnswer(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Ответ пользователя",
        operation_summary="Ответ на вопрос",
        request_body=UserAnswerSerializer,
        responses={
            200: openapi.Response('Ответ успешно сохранен', UserAnswerSerializer),
            400: openapi.Response('Ошибка при сохранении ответа')
        }
    )

    def post(self, request):
        serializer = UserAnswerSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Сохранился ответ"}, status=status.HTTP_200_OK)

        return Response({"message": "Не сохранился ответ", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
