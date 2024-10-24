from rest_framework import serializers
from gestion_comptes.models.type_autorite import TypeAutorite

class TypeAutoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeAutorite
        fields = ['id', 'nom', 'description']