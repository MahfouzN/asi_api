from rest_framework import serializers
from common.models.localisation import Localisation

class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = [
            'idLocalisation',
            'longitude',
            'latitude',
            'limiteNord',
            'limiteSud',
            'limiteEst',
            'limiteOuest',
            'nomDuLieu',
            'description'
        ]
        read_only_fields = ['idLocalisation']  # Assurez-vous que l'ID ne peut pas être modifié

