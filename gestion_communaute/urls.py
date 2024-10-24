from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gestion_communaute.views.activite_communautaire_view import ActiviteCommunautaireViewSet
from gestion_communaute.views.admin_publication_view import AdminPublicationViewSet
from gestion_communaute.views.annonce_view import AnnonceViewSet
from gestion_communaute.views.publication_view import PublicationViewSet
from gestion_communaute.views.signalement_publication_view import SignalementPublicationViewSet




app_name = "gestion_communaute"

router = DefaultRouter()
router.register(r'annonces', AnnonceViewSet,basename='annonce')
router.register(r'publications', PublicationViewSet, basename='publication')
router.register(r'activites-communautaires', ActiviteCommunautaireViewSet, basename='activite-communautaire')
router.register(r'admin-publications', AdminPublicationViewSet, basename='admin-publication')
router.register(r'signalements-publications', SignalementPublicationViewSet, basename='signalement-publication')

urlpatterns = [
    path('', include(router.urls)),
]