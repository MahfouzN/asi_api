from common.models.localisation import Localisation
from common.serializers.localisation_serilializers import LocalisationSerializer
from gestion_comptes.models.commune import Commune
from gestion_comptes.models.personne import Personne
from gestion_comptes.serializers.personne_serializers import PersonneSerializer
from rest_framework import serializers
from authentification.models import Compte


class CommuneRequestSerializer(serializers.ModelSerializer):
    localisationCommune = LocalisationSerializer()
    maire_telephone = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Commune
        fields = ['id', 'numOrdre', 'nomCommune', 'maire_telephone', 'localisationCommune']

    def create(self, validated_data):
        localisation_data = validated_data.pop('localisationCommune')
        maire_telephone = validated_data.pop('maire_telephone', None)
        localisation = Localisation.objects.create(**localisation_data)
        
        commune = Commune.objects.create(localisationCommune=localisation, **validated_data)
        
        if maire_telephone:
            try:
                compte = Compte.objects.get(telephone=maire_telephone)
                personne = compte.personne
                commune.maire = personne
                commune.save()
            except (Compte.DoesNotExist, Personne.DoesNotExist):
                pass  # Gérer l'erreur si le compte ou la personne n'existe pas
        
        return commune

    def update(self, instance, validated_data):
        localisation_data = validated_data.pop('localisationCommune', None)
        maire_telephone = validated_data.pop('maire_telephone', None)
        
        if localisation_data:
            localisation_serializer = LocalisationSerializer(instance.localisationCommune, data=localisation_data)
            if localisation_serializer.is_valid():
                localisation_serializer.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if maire_telephone:
            try:
                compte = Compte.objects.get(telephone=maire_telephone)
                personne = compte.personne
                instance.maire = personne
            except (Compte.DoesNotExist, Personne.DoesNotExist):
                pass  # Gérer l'erreur si le compte ou la personne n'existe pas
        
        instance.save()
        return instance

class CommuneResponseSerializer(serializers.ModelSerializer):
    localisationCommune = LocalisationSerializer()
    maire = PersonneSerializer(read_only=True)

    class Meta:
        model = Commune
        fields = ['id', 'numOrdre', 'nomCommune', 'maire', 'localisationCommune']
        
