from rest_framework import viewsets, permissions
from gestion_comptes.serializers.personne_serializers import PersonneSerializer
import logging
from common.models.action_log import ActionLog
from utils.api_response import api_response
from rest_framework import status as drf_status

logger = logging.getLogger(__name__)

class CitoyenRegistrationView(viewsets.GenericViewSet):
    serializer_class = PersonneSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        mutable_data = request.data.copy()
        mutable_data['role'] = 'citoyen'
        mutable_data['is_active'] = True
        serializer = self.get_serializer(data=mutable_data)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=instance,
            action="Inscription citoyen",
            details=f"Nouveau citoyen inscrit : {instance.telephone}"
            )
            return api_response("0000", "Inscription réussie", serializer.data)
    
        # Concaténer les erreurs du serializer
        error_messages = ', '.join([f"{field}: {', '.join(errors)}" for field, errors in serializer.errors.items()])
        return api_response("0002", f"Erreur lors de l'inscription: {error_messages}")