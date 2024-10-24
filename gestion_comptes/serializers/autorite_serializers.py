from rest_framework import serializers

from authentification.serializers.compte_serializer import CompteSerializer
from common.models.fichier import Fichier
from common.serializers.fichier_serilializers import FichierSerializer
from gestion_comptes.models.autorite import AutoriteCompetente
from gestion_comptes.models.type_autorite import TypeAutorite
from gestion_comptes.serializers.type_autorite_serializers import TypeAutoriteSerializer


class AutoriteCompetenteSerializer(serializers.ModelSerializer):

    photo = serializers.ImageField(write_only=True, required=False)
    class Meta:
        model = AutoriteCompetente
        fields = CompteSerializer.Meta.fields + ['nom','type_autorite', 'zone_competence','photo']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        photo = validated_data.pop('photo', None)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        
        if photo:
            fichier = Fichier.objects.create(
                nomFichier=photo.name,
                poidFichier=f"{photo.size / (1024 * 1024):.2f} MB",
                cheminFichier=photo,
                context='profil'
            )
            instance.photo = fichier
            instance.save()
        return instance

class AutoriteListSerializer(serializers.ModelSerializer):
    photo = FichierSerializer(read_only=True)  # Utilisez le serializer pour la photo

    class Meta:
        model = AutoriteCompetente
        fields = ['id','username', 'telephone', 'email', 'role', 'photo','is_active', 'date_joined','nom','type_autorite', 'zone_competence']  # Ajoutez d'autres champs si nécessaire