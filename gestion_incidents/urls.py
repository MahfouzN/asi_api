
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from gestion_incidents.views.incident_view import AutoriteIncidentViewSet, IncidentViewSet
from gestion_incidents.views.type_incident_view import TypeIncidentViewSet



app_name = "gestion_incidents"
router = DefaultRouter()



router = DefaultRouter()
router.register(r'incidents', IncidentViewSet, basename='incident')
router.register(r'autorite-incidents',AutoriteIncidentViewSet, basename='autorite-incident')
router.register(r'types-incidents', TypeIncidentViewSet, basename='type-incident')


urlpatterns = [
    path('', include(router.urls)),
]
