
from django.contrib import admin
from django.urls import path,include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static
from management.views import DashboardView

schema_view = get_schema_view(
    openapi.Info(
        title="PECHINCHOU API",
        default_version='v1',
        description="Api do sistema pechinchou.com.br",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="jefersonqueiroga@gmail.com"),
        license=openapi.License(name="Test License"),
    ),
    public=False,
    permission_classes=(permissions.IsAdminUser,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('autenticacao/', include('authentication.urls')),
    path('gerenciamento/', include('management.urls'), name='gerenciamento'),
    path('', include('accounts.urls')),
    
    path('produto/', include('product.urls')),
    path('api/produto/',include('product.api.urls')),
    path('api/gerenciamento/', include('management.api.urls')),
    path('api/grupos_whatsapp/', include('groupswhats.api.urls')),
    path('', DashboardView.as_view(), name='index'),
    path('social_auth/', include('social_auth.urls') ),
    path('api/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
