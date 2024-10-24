
from authentification.serializers.compte_serializer import CompteSerializer
from common.models.fichier import Fichier
from common.serializers.fichier_serilializers import FichierSerializer
from gestion_comptes.models.personne import Personne
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class PersonneSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    photo = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Personne
        fields = CompteSerializer.Meta.fields + ['nom', 'prenom', 'commune', 'password', 'photo']

    def create(self, validated_data):
        photo = validated_data.pop('photo', None)
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
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

    def update(self, instance, validated_data):
        photo = validated_data.pop('photo', None)
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        if photo:
            if instance.photo:
                instance.photo.delete()  # Supprime l'ancien fichier si existant
            fichier = Fichier.objects.create(
                nomFichier=photo.name,
                poidFichier=f"{photo.size / (1024 * 1024):.2f} MB",
                cheminFichier=photo,
                context='profil'
            )
            instance.photo = fichier
        
        instance.save()
        return instance
    

class PersonneListSerializer(serializers.ModelSerializer):
    photo = FichierSerializer(read_only=True)  # Utilisez le serializer pour la photo

    class Meta:
        model = Personne
        fields = ['id', 'telephone','nom','username','prenom', 'email', 'role', 'photo','is_active', 'date_joined']