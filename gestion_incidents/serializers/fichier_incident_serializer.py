from common.serializers.fichier_serilializers import FichierSerializer
from gestion_incidents.models.fichier_incident import FichierIncident
from rest_framework import serializers

class FichierIncidentSerializer(serializers.ModelSerializer):
    fichier = FichierSerializer(read_only=True)

    class Meta:
        model = FichierIncident
        fields = ['fichier']