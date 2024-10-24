"""
URL configuration for asi_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static

from gestion_comptes.views.autorite_pdf_view import GeneratePDFView
from gestion_comptes.views.statistiques_view import StatistiquesSystemeView


schema_view = get_schema_view(
    openapi.Info(
        title="Asi api",
        default_version='v1',
        description="Asi description",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
handler500 = 'utils.custom_error_view.custom_error_view'
urlpatterns = [
    path('asi/admin/', admin.site.urls),
    path('asi/statistiques/', StatistiquesSystemeView.as_view(), name='statistiques-systeme'),
    path('asi/authentification/', include('authentification.urls')),
    path('asi/gestion_comptes/', include('gestion_comptes.urls')),
    path('asi/gestion_incidents/', include('gestion_incidents.urls')),
    path('asi/gestion_communaute/', include('gestion_communaute.urls')),
    path('pdf/autorites/', GeneratePDFView.as_view(), name='generate_pdf_autorites'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
