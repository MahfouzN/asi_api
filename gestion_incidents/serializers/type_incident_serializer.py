from rest_framework import serializers
from common.serializers.fichier_serilializers import FichierSerializer
from gestion_incidents.models.type_incident import TypeIncident
from common.models.fichier import Fichier  # Importez le modèle Fichier
from gestion_comptes.serializers.type_autorite_serializers import TypeAutoriteSerializer

class TypeIncidentSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=True)  # Champ icon obligatoire

    class Meta:
        model = TypeIncident
        fields = '__all__'  

    def create(self, validated_data):
        icon = validated_data.pop('icon')
        print(f"Icon received: {icon}")
        # Gérer le fichier icon avant de sauvegarder l'instance
        fichier = Fichier.objects.create(
        nomFichier=icon.name,
        poidFichier=f"{icon.size / (1024 * 1024):.2f} MB",
        cheminFichier=icon,
        context='type_incident'
        )
        print(f"Fichier created: {fichier}")
        
        instance = self.Meta.model(**validated_data)
        instance.icon = fichier
        instance.save()
        return instance


    def update(self, instance, validated_data):
        icon = validated_data.pop('icon', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if icon:
            if instance.icon:
                instance.icon.delete()  # Supprime l'ancien fichier si existant
            fichier = Fichier.objects.create(
                nomFichier=icon.name,
                poidFichier=f"{icon.size / (1024 * 1024):.2f} MB",
                cheminFichier=icon,
                context='type_incident'
            )
            instance.icon = fichier

        instance.save()
        return instance
    
class TypeIncidentListSerializer(serializers.ModelSerializer):
    icon = FichierSerializer(read_only=True)
    type_autorite=TypeAutoriteSerializer()
    class Meta:
        model = TypeIncident
        fields = ['id','code','nom', 'description', 'type_autorite', 'icon','is_active']