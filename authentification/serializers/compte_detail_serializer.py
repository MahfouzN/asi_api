

from authentification.models import Compte
from rest_framework import serializers

from gestion_comptes.models.autorite import AutoriteCompetente
from gestion_comptes.models.personne import Personne
from gestion_comptes.serializers.autorite_serializers import AutoriteCompetenteSerializer
from gestion_comptes.serializers.personne_serializers import PersonneSerializer

class CompteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        fields = ['id', 'telephone', 'email','username', 'role', 'photo','is_active']

    def to_representation(self, instance):
        if isinstance(instance, Personne):
            return PersonneSerializer(instance).data
        elif isinstance(instance, AutoriteCompetente):
            return AutoriteCompetenteSerializer(instance).data
        else:
            return super().to_representation(instance)