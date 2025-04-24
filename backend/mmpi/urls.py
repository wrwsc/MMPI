from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import render
from Api.deleteUserAnswer.views import ApiDeleteUserAnswer
from Api.getUserAnswers.views import ApiGetUserAnswers
from Api.postUserAnswer.views import ApiPostUserAnswer
from Api.putUserAnswer.views import ApiPutUserAnswer
from Api.RegisterUserApi.views import RegisterUserApi
from rest_framework.authtoken.views import obtain_auth_token


schema_view = get_schema_view(
    openapi.Info(
        title="MMPI API",
        default_version="v1",
        description="Документация API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def empty_page(request):
    return render(request, "empty.html")

def index_page(request):
    return render(request, 'index.html')

def test_page(request):
    return render(request, 'test.html')

urlpatterns = [
    path("", index_page),
    path("admin/", admin.site.urls),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path('api/answer-post/<int:user_id>/', ApiPostUserAnswer.as_view(), name='post-user-answer'),
    path('api/answer-get/<int:user_id>/', ApiGetUserAnswers.as_view(), name='get-user-answers'),
    path('api/answer-delete/<int:user_id>/<int:question_id>/', ApiDeleteUserAnswer.as_view(), name='delete-user-answer'),
    path('api/answer-put/<int:user_id>/<int:question_id>/<str:answer>/', ApiPutUserAnswer.as_view(), name='put-user-answer'),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path('api/register/', RegisterUserApi.as_view(), name='register'),
    path('test/', test_page, name='test-page'),
]
