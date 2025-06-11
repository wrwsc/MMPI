from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from Api.continueTest.views import ApiContinueTest
from Api.deleteUserAnswer.views import ApiDeleteUserAnswer
from Api.getUserAnswers.views import ApiGetUserAnswers
from Api.graphExportAPIView.views import GraphExportAPIView
from Api.graphImageApiView.views import GraphImageAPIView
from Api.postUserAnswer.views import ApiPostUserAnswer
from Api.putUserAnswer.views import ApiPutUserAnswer
from Api.RegisterUserApi.views import RegisterUserApi
from rest_framework.authentication import TokenAuthentication
from Api.resetUserAnswers.views import ApiResetUserAnswers
from Api.testStatusAnswer.views import ApiTestStatus




urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/answer-post/<int:user_id>/', ApiPostUserAnswer.as_view(), name='post-user-answer'),
    path('api/answer-get/<int:user_id>/', ApiGetUserAnswers.as_view(), name='get-user-answers'),
    path('api/answer-delete/<int:user_id>/<int:question_id>/', ApiDeleteUserAnswer.as_view(), name='delete-user-answer'),
    path('api/answer-put/<int:user_id>/<int:question_id>/<str:answer>/', ApiPutUserAnswer.as_view(), name='put-user-answer'),
    path('api/register/', RegisterUserApi.as_view(), name='register'),
    path('api/export-graph/<int:user_id>/', GraphExportAPIView.as_view(), name='export-graph'),
    path('api/answer-reset/<int:user_id>/', ApiResetUserAnswers.as_view(), name='reset-user-answers'),
    path('api/test-status/<int:user_id>/', ApiTestStatus.as_view(), name='test-status'),
    path('api/test-continue/<int:user_id>/', ApiContinueTest.as_view(), name='test-continue'),
    path('api/graph/image/<int:user_id>/', GraphImageAPIView.as_view(), name='graph-image'),
]
