from rest_framework import viewsets, permissions
from gestion_incidents.models.type_incident import TypeIncident
from gestion_incidents.serializers.type_incident_serializer import TypeIncidentListSerializer, TypeIncidentSerializer
from common.models.action_log import ActionLog
from utils.api_response import api_response

class TypeIncidentViewSet(viewsets.ModelViewSet):
    serializer_class = TypeIncidentSerializer  # Serializer par défaut

    def get_queryset(self):
        # Si l'utilisateur est superadmin, récupérer tous les types d'incidents
        if self.request.user.is_superadmin:
            return TypeIncident.objects.all()
        # Sinon, récupérer uniquement les types actifs
        return TypeIncident.objects.filter(is_active=True)

    def get_serializer_class(self):
        # Utiliser un serializer différent pour l'action 'list'
        if self.action == 'list':
            return TypeIncidentListSerializer  # Serializer spécifique pour la liste
        return TypeIncidentSerializer  # Serializer par défaut

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response("0000", "Liste des types d'incidents récupérée avec succès", serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.is_superadmin:
            return api_response("0001", "Vous n'avez pas la permission d'effectuer cette action.")
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action="Création de type d'incident",
                details=f"Type d'incident '{instance.nom}' créé"
            )
            return api_response("0000", "Type d'incident créé avec succès", serializer.data)
        return api_response("0002", "Erreur lors de la création du type d'incident", serializer.errors)

    def update(self, request, *args, **kwargs):
        if not request.user.is_superadmin:
            return api_response("0001", "Vous n'avez pas la permission d'effectuer cette action.")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            updated_instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action="Modification de type d'incident",
                details=f"Type d'incident '{updated_instance.nom}' modifié"
            )
            return api_response("0000", "Type d'incident modifié avec succès", serializer.data)
        return api_response("0002", "Erreur lors de la modification du type d'incident", serializer.errors)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superadmin:
            return api_response("0001", "Vous n'avez pas la permission d'effectuer cette action.")
        instance = self.get_object()
        nom_type_incident = instance.nom
        instance.delete()
        ActionLog.objects.create(
            user=request.user,
            action="Suppression de type d'incident",
            details=f"Type d'incident '{nom_type_incident}' supprimé"
        )
        return api_response("0000", "Type d'incident supprimé avec succès")
