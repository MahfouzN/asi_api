from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from gestion_communaute.models.inscription_activite import Inscription
from gestion_communaute.serializers.inscription_activite_serializer import InscriptionSerializer


class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'responsable':
            return Inscription.objects.filter(activite__commune=user.personne.commune)
        elif user.role == 'citoyen':
            return Inscription.objects.filter(participant=user.personne)
        return super().get_queryset()