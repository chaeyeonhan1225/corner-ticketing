from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="방구석 티켓팅",
        default_version="0.0.1",
        description="방구석 티켓팅 개발 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="gkscodus11@gmail.com"),  # 부가정보
        license=openapi.License(name="mit"),  # 부가정보
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    path("admin/", admin.site.urls),
    path("api/users/", include("user.urls")),
    path("api/events/", include("event.urls")),
    path("api/common/", include("common.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("silk/", include("silk.urls")),
    ]
