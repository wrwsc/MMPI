from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import render

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

urlpatterns = [
    path("", empty_page),
    path("admin/", admin.site.urls),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]
