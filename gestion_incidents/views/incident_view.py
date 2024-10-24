from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from common.models.action_log import ActionLog
from gestion_communaute.models.publication import Publication
from gestion_comptes.models.autorite import AutoriteCompetente
from gestion_incidents.models.incident import Incident, StatutTraitement
from gestion_incidents.serializers.incident_serializer import IncidentRequestSerializer, IncidentResponseSerializer
from utils.api_response import api_response







class IncidentViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'citoyen':
            return Incident.objects.filter(signaleur=user)
        elif user.role == 'autorite':
            autorite = AutoriteCompetente.objects.get(compte_ptr=user)
            return Incident.objects.filter(commune=autorite.zone_competence, type_incident__type_autorite=autorite.type_autorite)
        return Incident.objects.none()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return IncidentRequestSerializer
        return IncidentResponseSerializer

    def perform_create(self, serializer):
        incident = serializer.save()
        ActionLog.objects.create(
            user=self.request.user,
            action="Création d'incident",
            details=f"Incident {incident.titre} créé"
        )

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = IncidentResponseSerializer(instance)
            return api_response("0000", "Incident créée avec succès", response_serializer.data)
        return api_response("0002", "Erreur lors de la création de l'incident", serializer.errors)




    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response("0000", "Liste des incidents récupérée avec succès", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response("0000", "Détails de l'incident récupérés avec succès", serializer.data)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            ActionLog.objects.create(
                user=request.user,
                action="Modification d'incident",
                details=f"Incident {instance.titre} modifié"
            )
            return api_response("0000", "Incident modifié avec succès", serializer.data)
        return api_response("0002", "Erreur lors de la modification de l'incident", serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        titre_incident = instance.titre
        self.perform_destroy(instance)
        ActionLog.objects.create(
            user=request.user,
            action="Suppression d'incident",
            details=f"Incident {titre_incident} supprimé"
        )
        return api_response("0000", "Incident supprimé avec succès")


class AutoriteIncidentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]


    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return IncidentRequestSerializer
        return IncidentResponseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'autorite':
            autorite = AutoriteCompetente.objects.get(compte_ptr=user)
            return Incident.objects.filter(commune=autorite.zone_competence, type_incident__type_autorite=autorite.type_autorite)
        return Incident.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response("0000", "Liste des incidents récupérée avec succès", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response("0000", "Détails de l'incident récupérés avec succès", serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            ActionLog.objects.create(
                user=request.user,
                action="Modification d'incident par l'autorité",
                details=f"Incident {instance.titre} modifié"
            )
            return api_response("0000", "Incident modifié avec succès", serializer.data)
        return api_response("0002", "Erreur lors de la modification de l'incident", serializer.errors)

    @action(detail=True, methods=['post'])
    def changer_statut(self, request, pk=None):
        incident = self.get_object()
        nouveau_statut = request.data.get('statut')
        if nouveau_statut not in StatutTraitement.values:
            return api_response("0002", "Statut invalide")
        
        incident.statut = nouveau_statut
        incident.save()

        ActionLog.objects.create(
            user=request.user,
            action="Changement de statut d'incident",
            details=f"Statut de l'incident {incident.titre} changé à {nouveau_statut}"
        )

        if nouveau_statut == StatutTraitement.EN_TRAITEMENT and not incident.autorite_en_charge:
            incident.autorite_en_charge = request.user.autoritecompetente
        incident.statut = nouveau_statut
        incident.save()
        ActionLog.objects.create(
        user=request.user,
        action="Changement de statut d'incident",
        details=f"Statut de l'incident {incident.titre} changé à {nouveau_statut}"
        )

        if nouveau_statut == StatutTraitement.TRAITE:
            rapport = Publication.objects.create(
                titre=f"Rapport pour {incident.titre}",
                description="Rapport à compléter",
                auteur=request.user,
                commune=incident.commune,
                est_publie=False,
                est_active=True,

            )
            rapport.fichiers.set(incident.fichiers.all())
            ActionLog.objects.create(
                user=request.user,
                action="Création de rapport d'incident",
                details=f"Rapport créé pour l'incident {incident.titre}"
            )
            return api_response("0000", "Statut mis à jour et rapport créé", )

        return api_response("0000", "Statut mis à jour", IncidentResponseSerializer(incident).data)