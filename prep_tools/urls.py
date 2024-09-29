from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from notes.views import NoteViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("", NoteViewSet, basename="notes")
schema_view = get_schema_view(
    openapi.Info(
        title="Notes API",
        default_version='v1',
        description="This is a simple Notes API",

    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path("notes/", include("notes.urls")),
    path("auth/", include("accounts.urls")),
    path("notez/", include(router.urls)),
    path("", include("tools.urls"))
]
