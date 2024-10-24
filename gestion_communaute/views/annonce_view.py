from rest_framework import viewsets, permissions
from gestion_communaute.models.annonce import Annonce
from gestion_communaute.serializers.annonce_serializer import AnnonceListSerializer, AnnonceSerializer
from common.models.action_log import ActionLog
from utils.api_response import api_response

class AnnonceViewSet(viewsets.ModelViewSet):
    serializer_class = AnnonceSerializer  # Serializer par défaut

    def get_queryset(self):
        # Récupérer uniquement les annonces actives
        queryset = Annonce.objects.filter(is_active=True)

        # Si l'utilisateur n'est pas un administrateur, filtrer par commune
        if not self.request.user.is_superadmin:
            # Supposons que l'utilisateur a un attribut 'commune' pour filtrer
            commune = self.request.user.personne.commune
            queryset = queryset.filter(visible_dans_commune=commune) | queryset.filter(visible_dans_commune__isnull=True)

        return queryset

    def get_serializer_class(self):
        # Utiliser un serializer différent pour l'action 'list'
        if self.action == 'list':
            return AnnonceListSerializer  # Serializer spécifique pour la liste
        return AnnonceSerializer  # Serializer par défaut

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response("0000", "Liste des  annonces récupérée avec succès", serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return api_response("0001", "Vous n'avez pas la permission d'effectuer cette action.")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action="Création d'annonce",
                details=f"Annonce '{instance.nom}' créé"
            )
            return api_response("0000", "Annonce créée avec succès", serializer.data)
        return api_response("0002", "Erreur lors de la création d'une annonce", serializer.errors)

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
                action="Modification de type d'une annonce",
                details=f"Annonce '{updated_instance.nom}' modifié"
            )
            return api_response("0000", "Annonce modifié avec succès", serializer.data)
        return api_response("0002", "Erreur lors de la modification d'une annonce", serializer.errors)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superadmin:
            return api_response("0001", "Vous n'avez pas la permission d'effectuer cette action.")
        instance = self.get_object()
        instance.delete()
        ActionLog.objects.create(
            user=request.user,
            action="Suppression d'une annonce",
            details=f"Annonce '{instance.nom}' supprimé"
        )
        return api_response("0000", "Annonce supprimée avec succès")
