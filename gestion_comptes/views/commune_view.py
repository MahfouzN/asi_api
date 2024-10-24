
from common.models.permission import IsSuperAdminOrAdminForOwnCommune
from gestion_comptes.models.commune import Commune
from gestion_comptes.serializers.commune_serializers import *
from authentification.views.compte_view import *
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist

from common.models.permission import IsSuperAdminOrAdminForOwnCommune
from gestion_comptes.models.commune import Commune
from gestion_comptes.serializers.commune_serializers import *
from authentification.views.compte_view import *
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from common.models.action_log import ActionLog
from utils.api_response import api_response
from rest_framework.permissions import AllowAny

class CommuneViewSet(viewsets.ModelViewSet):
    queryset = Commune.objects.all()

    def get_permissions(self):
        # Permet l'accès libre uniquement pour la liste des communes
        if self.action == 'list':
            return [AllowAny()]
        # Pour les autres actions, restreindre l'accès
        return [IsSuperAdminOrAdminForOwnCommune()] 


    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommuneRequestSerializer
        return CommuneResponseSerializer

    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':  # Tous les utilisateurs peuvent voir la liste
            return Commune.objects.all()
        
        if user.is_superadmin:
            return Commune.objects.all()
        
        if user.role == 'administrateur':
            try:
                return Commune.objects.filter(id=user.personne.commune.id)
            except ObjectDoesNotExist:
                return Commune.objects.none()
        
        return Commune.objects.none()

    def create(self, request, *args, **kwargs):
        if not request.user.is_superadmin:
            return api_response("0002", "Seul le super administrateur peut créer des communes.")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action="Création de commune",
                details=f"Commune {instance.nomCommune} créée"
            )
            response_serializer = CommuneResponseSerializer(instance)
            return api_response("0000", "Commune créée avec succès", response_serializer.data)
        return api_response("0002", "Erreur lors de la création de la commune", serializer.errors)

    def update(self, request, *args, **kwargs):
        if not request.user.is_superadmin:
            return api_response("0002", "Seul le super administrateur peut modifier des communes.")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            updated_instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action="Modification de commune",
                details=f"Commune {updated_instance.nomCommune} modifiée"
            )
            response_serializer = CommuneResponseSerializer(updated_instance)
            return api_response("0000", "Commune modifiée avec succès", response_serializer.data)
        return api_response("0002", "Erreur lors de la modification de la commune", serializer.errors)

    def perform_destroy(self, instance):
        if not self.request.user.is_superadmin:
            raise PermissionDenied("Seul le super administrateur peut supprimer des communes.")
        nom_commune = instance.nomCommune
        instance.delete()
        ActionLog.objects.create(
            user=self.request.user,
            action="Suppression de commune",
            details=f"Commune {nom_commune} supprimée"
        )
        return api_response("0000", "Commune supprimée avec succès")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response("0000", "Liste des communes récupérée avec succès", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response("0000", "Détails de la commune récupérés avec succès", serializer.data)