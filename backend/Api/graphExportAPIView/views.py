from Dal.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Dal.tables.table import M_table, delta_table
from Logic.calculate.saveTScores import save_user_t_scores
from Logic.calculate.scoring import (
    calculate_t_scores, calculate_raw_scores,
    apply_corrections, generate_graph, generate_pdf, has_completed_all_questions
)
from rest_framework.exceptions import AuthenticationFailed
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class GraphExportAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        print(f"Авторизованный пользователь: {request.user}")
        try:
            target_user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        current_user = User.objects.get(django_user=request.user)
        if not request.user.is_superuser and current_user.user_id != target_user.user_id:
            return Response({"message": "Вы не можете получить данные другого пользователя"}, status=status.HTTP_403_FORBIDDEN)

        if not has_completed_all_questions(target_user):
            return Response(
                {"message": "Пользователь не ответил на все вопросы"},
                status=status.HTTP_400_BAD_REQUEST
            )

        raw_scores = calculate_raw_scores(target_user)
        corrected_scores = apply_corrections(raw_scores)
        t_scores = calculate_t_scores(corrected_scores, M_table, delta_table, target_user.sex)

        original_t_value = request.query_params.get("original_T", None)
        if original_t_value:
            try:
                original_t_value = float(original_t_value)
            except ValueError:
                return Response({"message": "Неверное значение для original_T"}, status=status.HTTP_400_BAD_REQUEST)

        save_user_t_scores(target_user, t_scores, raw_scores, original_t_value)

        graph_file = generate_graph(t_scores)
        pdf_file = generate_pdf(graph_file, target_user)

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="test_results.pdf"'
        return response
