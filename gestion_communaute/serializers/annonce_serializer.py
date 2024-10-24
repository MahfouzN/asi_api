from rest_framework import serializers
from common.serializers.fichier_serilializers import FichierSerializer
from gestion_communaute.models.annonce import Annonce
from gestion_comptes.serializers.commune_serializers import CommuneResponseSerializer
from gestion_incidents.models.type_incident import TypeIncident
from common.models.fichier import Fichier  # Importez le modèle Fichier
from gestion_comptes.serializers.type_autorite_serializers import TypeAutoriteSerializer

class AnnonceSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)  # Champ icon obligatoire

    class Meta:
        model = Annonce
        fields = '__all__'  

    def create(self, validated_data):
        image = validated_data.pop('image')
    
        # Gérer le fichier icon avant de sauvegarder l'instance
        fichier = Fichier.objects.create(
        nomFichier=image.name,
        poidFichier=f"{image.size / (1024 * 1024):.2f} MB",
        cheminFichier=image,
        context='communaute_annonce'
        )
    
        
        instance = self.Meta.model(**validated_data)
        instance.image = fichier
        instance.save()
        return instance


    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if image:
            if instance.image:
                instance.image.delete()  # Supprime l'ancien fichier si existant
            fichier = Fichier.objects.create(
                nomFichier=image.name,
                poidFichier=f"{image.size / (1024 * 1024):.2f} MB",
                cheminFichier=image,
                context='communaute_annonce'
            )
            instance.image = fichier

        instance.save()
        return instance
    
class AnnonceListSerializer(serializers.ModelSerializer):
    image = FichierSerializer(read_only=True)
    visible_dans_commune= CommuneResponseSerializer()
    class Meta:
        model = Annonce
        fields = ['id','nom', 'description','image','date_creation','is_active','visible_dans_commune']