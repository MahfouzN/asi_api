from common.models.permission import IsSuperAdminOrAdminForOwnCommune
from gestion_comptes.models.type_autorite import TypeAutorite
from gestion_comptes.serializers.type_autorite_serializers import TypeAutoriteSerializer
from authentification.views.compte_view import *
from rest_framework import viewsets, permissions
from common.models.action_log import ActionLog
from utils.api_response import api_response

class TypeAutoriteViewSet(viewsets.ModelViewSet):
    queryset = TypeAutorite.objects.all()
    serializer_class = TypeAutoriteSerializer
    permission_classes = [IsSuperAdminOrAdminForOwnCommune]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response("0000", "Liste des types d'autorité récupérée avec succès", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response("0000", "Détails du type d'autorité récupérés avec succès", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action="Création de type d'autorité",
                details=f"Type d'autorité '{instance.nom}' créé"
            )
            return api_response("0000", "Type d'autorité créé avec succès", serializer.data)
        return api_response("0002", "Erreur lors de la création du type d'autorité", serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            updated_instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action="Modification de type d'autorité",
                details=f"Type d'autorité '{updated_instance.nom}' modifié"
            )
            return api_response("0000", "Type d'autorité modifié avec succès", serializer.data)
        return api_response("0002", "Erreur lors de la modification du type d'autorité", serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        nom_type_autorite = instance.nom
        instance.delete()
        ActionLog.objects.create(
            user=request.user,
            action="Suppression de type d'autorité",
            details=f"Type d'autorité '{nom_type_autorite}' supprimé"
        )
        return api_response("0000", "Type d'autorité supprimé avec succès")