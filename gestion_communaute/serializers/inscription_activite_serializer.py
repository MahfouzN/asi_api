from rest_framework import serializers

from gestion_communaute.models.inscription_activite import Inscription

class InscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = '__all__'