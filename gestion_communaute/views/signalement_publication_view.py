from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from common.models.permission import IsSuperAdminOrAdminForOwnCommune
from gestion_communaute.models.signalementPublication import SignalementPublication
from gestion_communaute.serializers.signalement_publication_serializer import SignalementPublicationSerializer
from common.models.action_log import ActionLog
from utils.api_response import api_response

class SignalementPublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SignalementPublication.objects.filter(est_traite=False)
    serializer_class = SignalementPublicationSerializer
    permission_classes = [IsSuperAdminOrAdminForOwnCommune]

    def get_queryset(self):
        queryset = SignalementPublication.objects.filter(est_traite=False)
        if not self.request.user.is_superadmin:
            admin_commune = self.request.user.personne.commune
            queryset = queryset.filter(publication__commune=admin_commune)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response("0000", "Liste des signalements récupérée avec succès", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response("0000", "Détails du signalement récupérés avec succès", serializer.data)

    @action(detail=True, methods=['post'])
    def marquer_traite(self, request, pk=None):
        signalement = self.get_object()
        signalement.est_traite = True
        signalement.save()
        
        ActionLog.objects.create(
            user=request.user,
            action="Signalement traité",
            details=f"Signalement {signalement.id} marqué comme traité"
        )
        
        return api_response("0000", "Signalement marqué comme traité", {'est_traite': signalement.est_traite})