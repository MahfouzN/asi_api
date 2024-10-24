from rest_framework import serializers
from common.models.fichier import Fichier

class FichierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fichier
        fields = ['idFichier', 'nomFichier', 'poidFichier', 'cheminFichier', 'typeFichier']
