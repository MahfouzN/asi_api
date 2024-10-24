from rest_framework import serializers
from authentification.models import Compte
from common.models.fichier import Fichier
from common.serializers.fichier_serilializers import FichierSerializer

class CompteSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Compte
        fields = ['id', 'telephone', 'email','username','role', 'photo', 'is_active', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        photo = validated_data.pop('photo', None)
        password = validated_data.pop('password', None)
        instance = Compte(**validated_data)
        if password:
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
                instance.photo.delete()
            fichier = Fichier.objects.create(
                nomFichier=photo.name,
                poidFichier=f"{photo.size / (1024 * 1024):.2f} MB",
                cheminFichier=photo,
                context='profil'
            )
            instance.photo = fichier
        
        instance.save()
        return instance
    

class CompteListSerializer(serializers.ModelSerializer):
    photo = FichierSerializer(read_only=True)

    class Meta:
        model = Compte
        fields = ['id', 'telephone', 'email','username', 'role', 'photo','is_active', 'date_joined']