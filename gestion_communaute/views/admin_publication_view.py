from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from common.models.permission import IsSuperAdminOrAdminForOwnCommune
from gestion_communaute.models.publication import Publication
from gestion_communaute.serializers.publication_citoyen_serilializers import  PublicationSerializer
from common.models.action_log import ActionLog
from utils.api_response import api_response

class AdminPublicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperAdminOrAdminForOwnCommune]

    def get_queryset(self):
        queryset = Publication.objects.all()
        if not self.request.user.is_superadmin:
            admin_commune = self.request.user.personne.commune
            queryset = queryset.filter(commune=admin_commune)
        return queryset

    def get_serializer_class(self):
        return PublicationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response("0000", "Liste des publications récupérée avec succès", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response("0000", "Détails de la publication récupérés avec succès", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action="Création de publication par admin",
                details=f"Publication '{instance.titre}' créée par admin"
            )
            return api_response("0000", "Publication créée avec succès", serializer.data, status.HTTP_201_CREATED)
        return api_response("0002", "Erreur lors de la création de la publication", serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            updated_instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action="Modification de publication par admin",
                details=f"Publication '{updated_instance.titre}' modifiée par admin"
            )
            return api_response("0000", "Publication modifiée avec succès", serializer.data)
        return api_response("0002", "Erreur lors de la modification de la publication", serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        titre_publication = instance.titre
        instance.delete()
        ActionLog.objects.create(
            user=request.user,
            action="Suppression de publication par admin",
            details=f"Publication '{titre_publication}' supprimée par admin"
        )
        return api_response("0000", "Publication supprimée avec succès")

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        publication = self.get_object()
        publication.est_active = not publication.est_active
        publication.save()
        
        action = "activée" if publication.est_active else "désactivée"
        ActionLog.objects.create(
            user=request.user,
            action=f"Publication {action} par admin",
            details=f"Publication '{publication.titre}' {action} par admin"
        )
        
        return api_response("0000", f"Publication {action} avec succès", {'est_active': publication.est_active})