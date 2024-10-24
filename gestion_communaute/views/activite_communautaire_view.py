from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from common.models.action_log import ActionLog
from gestion_communaute.models.activite_communautaire import ActiviteCommunautaire
from gestion_communaute.models.inscription_activite import Inscription
from gestion_communaute.serializers.activite_communautaire_serializer import ActiviteCommunautaireListSerializer, ActiviteCommunautaireSerializer
from gestion_comptes.models.personne import Personne
from gestion_comptes.serializers.personne_serializers import PersonneSerializer
from utils.api_response import api_response
from django.db.models import Count, Prefetch

class ActiviteCommunautaireViewSet(viewsets.ModelViewSet):
    queryset = ActiviteCommunautaire.objects.all()
    serializer_class = ActiviteCommunautaireSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = ActiviteCommunautaire.objects.prefetch_related(
            Prefetch('participants', queryset=Personne.objects.all()),
            Prefetch('inscriptions', queryset=Inscription.objects.select_related('participant')),
        )

        if user.role == 'responsable':
            return queryset.filter(commune=user.personne.commune)
        elif user.role == 'citoyen':
            return queryset.filter(commune=user.personne.commune, inscriptions_actives=True)
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ActiviteCommunautaireSerializer
        return ActiviteCommunautaireListSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        ActionLog.objects.create(
            user=self.request.user,
            action="Création d'activité communautaire",
            details=f"Activité communautaire {instance.titre} créée"
        )

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_serializer = ActiviteCommunautaireListSerializer(serializer.instance)
            return api_response("0000", "Activité communautaire créée avec succès", response_serializer.data)
        return api_response("0002", "Erreur lors de la création de l'activité communautaire", serializer.errors)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response("0000", "Liste des activités communautaires récupérée avec succès", serializer.data)

    @action(detail=True, methods=['post'])
    def inscrire(self, request, pk=None):
        activite = self.get_object()
        utilisateur = request.user.personne

        if not activite.peut_s_inscrire():
            return api_response("0002", "Les inscriptions ne sont pas ouvertes pour cette activité.", None)

        if Inscription.objects.filter(activite=activite, participant=utilisateur).exists():
            return api_response("0002", "Vous êtes déjà inscrit à cette activité.", None)
        activite.participants.add(utilisateur)
        return api_response("0000", "Inscription réussie.", None)

    @action(detail=True, methods=['post'])
    def desinscrire(self, request, pk=None):
        activite = self.get_object()
        utilisateur = request.user.personne

        inscription = Inscription.objects.filter(activite=activite, participant=utilisateur).first()
        if not inscription:
            return api_response("0002", "Vous n'êtes pas inscrit à cette activité.", None)

        inscription.delete()
        return api_response("0000", "Désinscription réussie.", None)

    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        activite = self.get_object()
        participants = activite.inscriptions.all().select_related('participant')
        serializer = PersonneSerializer([inscription.participant for inscription in participants], many=True)
        return api_response("0000", "Participants récupérés avec succès", serializer.data)