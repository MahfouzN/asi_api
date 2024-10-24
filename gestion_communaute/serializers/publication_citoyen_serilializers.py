from rest_framework import serializers
from authentification.serializers.compte_serializer import CompteListSerializer
from common.models.fichier import Fichier
from common.serializers.fichier_serilializers import FichierSerializer
from gestion_communaute.models.publication import Publication
from gestion_comptes.models.personne import Personne
from gestion_comptes.serializers.commune_serializers import CommuneResponseSerializer


class PublicationSerializer(serializers.ModelSerializer):
    fichiers = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)

    class Meta:
        model = Publication
        fields = ['id', 'titre', 'description', 'auteur', 'commune', 'date_creation', 'date_mise_a_jour', 'est_publie', 'est_active', 'fichiers']
        read_only_fields = ['auteur', 'commune', 'date_creation', 'date_mise_a_jour']

    
    def create(self, validated_data):
        fichiers = validated_data.pop('fichiers', [])
        validated_data.pop('est_active', None)
        validated_data.pop('est_publie', None)
        auteur = self.context['request'].user
        
        try:
            personne = Personne.objects.get(compte_ptr_id=auteur.id)
            commune = personne.commune
        except Personne.DoesNotExist:
            raise serializers.ValidationError("Utilisateur invalide")
        publication = Publication.objects.create(
            **validated_data,
            auteur=auteur,
            commune=commune,
            est_publie=True, 
            est_active=True,
        )
        for fichier in fichiers:
            fichier_obj = Fichier.objects.create(
                nomFichier=fichier.name,
                poidFichier=f"{fichier.size / (1024 * 1024):.2f} MB",
                cheminFichier=fichier,
                context='publication'
            )
            publication.fichiers.add(fichier_obj)
        return publication


class PublicationListSerializer(serializers.ModelSerializer):
    auteur = CompteListSerializer(read_only=True)
    fichiers = FichierSerializer(many=True, read_only=True)
    commune = CommuneResponseSerializer(read_only=True)
  

    class Meta:
        model = Publication
        fields = ['id', 'titre', 'description','commune','auteur','date_creation', 'date_mise_a_jour', 'est_publie', 'est_active', 'fichiers']

    def get_nombre_likes(self, obj):
        return obj.likes.count()
