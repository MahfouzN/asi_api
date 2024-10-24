from rest_framework import serializers

from gestion_communaute.models.signalementPublication import SignalementPublication


class SignalementPublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalementPublication
        fields = ['__all__']

