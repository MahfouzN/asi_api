from rest_framework import serializers
from common.models.fichier import Fichier
from common.models.localisation import Localisation
from common.serializers.fichier_serilializers import FichierSerializer
from common.serializers.localisation_serilializers import LocalisationSerializer
from gestion_comptes.models.personne import Personne
from gestion_comptes.serializers.autorite_serializers import AutoriteListSerializer
from gestion_comptes.serializers.commune_serializers import CommuneResponseSerializer
from gestion_comptes.serializers.personne_serializers import PersonneSerializer
from gestion_incidents.models.incident import Incident
from gestion_incidents.models.type_incident import TypeIncident
from gestion_incidents.serializers.fichier_incident_serializer import FichierIncidentSerializer
from gestion_incidents.serializers.type_incident_serializer import TypeIncidentListSerializer, TypeIncidentSerializer

class IncidentRequestSerializer(serializers.ModelSerializer):
    fichiers = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    localisation = serializers.JSONField()
    type_incident_code = serializers.CharField(write_only=True)

    class Meta:
        model = Incident
        fields = ['titre', 'description', 'date_incident', 'type_incident_code', 'localisation', 'fichiers']

    def create(self, validated_data):
        type_incident_code = validated_data.pop('type_incident_code')
        type_incident = TypeIncident.objects.get(code=type_incident_code)
        fichiers = validated_data.pop('fichiers', [])
        localisation_data = validated_data.pop('localisation')
        
        localisation = Localisation.objects.create(**localisation_data)

        compte_signaleur = self.context['request'].user
        
        try:
            personne = Personne.objects.get(compte_ptr_id=compte_signaleur.id)
            commune = personne.commune
        except Personne.DoesNotExist:
            raise serializers.ValidationError("Utilisateur invalide")

        incident = Incident.objects.create(
            **validated_data,
            localisation=localisation,
            signaleur=personne,
            commune=commune,
            type_incident=type_incident,
        )

        for fichier in fichiers:
            fichier_obj = Fichier.objects.create(
                nomFichier=fichier.name,
                poidFichier=f"{fichier.size / (1024 * 1024):.2f} MB",
                cheminFichier=fichier,
                context='incident'
            )
            incident.fichier_incidents.create(fichier=fichier_obj)

        return incident

class IncidentResponseSerializer(serializers.ModelSerializer):
    localisation = LocalisationSerializer()
    fichiers = serializers.SerializerMethodField()
    type_incident=TypeIncidentListSerializer()
    signaleur=PersonneSerializer()
    commune=CommuneResponseSerializer()
    autorite_en_charge=AutoriteListSerializer()


    class Meta:
        model = Incident
        fields = ['id', 'titre', 'description', 'date_incident', 'type_incident', 'signaleur', 'commune', 'localisation', 'statut', 'fichiers','autorite_en_charge']
        read_only_fields = ['signaleur', 'autorite_en_charge','commune', 'fichiers']
    
    def get_fichiers(self, obj):
        fichier_incidents = obj.fichier_incidents.all()
        fichiers = [fichier_incident.fichier for fichier_incident in fichier_incidents]
        return FichierSerializer(fichiers, many=True,read_only=True).data
