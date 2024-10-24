
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authentification.views.compte_view import CompteDetailView
from common.views.action_log_views import ActionLogViewSet
from gestion_comptes.views.administrateur_view import AdminCompteViewSet
from gestion_comptes.views.autorite_pdf_view import GeneratePDFView
from gestion_comptes.views.autorite_view import AutoriteViewSet
from gestion_comptes.views.commune_view import CommuneViewSet
from gestion_comptes.views.type_autorite_view import TypeAutoriteViewSet


app_name = "gestion_comptes"
router = DefaultRouter()



# Ajouter vos viewsets ici
router = DefaultRouter()


router.register(r'comptes', AdminCompteViewSet)
router.register(r'compte-detail', CompteDetailView, basename='compte-detail')
router.register(r'autorites', AutoriteViewSet)
router.register(r'types-autorite', TypeAutoriteViewSet)
router.register(r'communes', CommuneViewSet)
router.register(r'action-logs', ActionLogViewSet)


urlpatterns = [
    path('', include(router.urls)),

]
