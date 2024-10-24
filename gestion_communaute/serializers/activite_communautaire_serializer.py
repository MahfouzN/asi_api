from rest_framework import serializers

from common.models.fichier import Fichier
from common.models.localisation import Localisation
from common.serializers.fichier_serilializers import FichierSerializer
from common.serializers.localisation_serilializers import LocalisationSerializer
from gestion_communaute.models.activite_communautaire import ActiviteCommunautaire
from gestion_comptes.models.personne import Personne
from gestion_comptes.serializers.commune_serializers import CommuneResponseSerializer
from gestion_comptes.serializers.personne_serializers import PersonneListSerializer, PersonneSerializer

import logging

logger = logging.getLogger(__name__)

class ActiviteCommunautaireSerializer(serializers.ModelSerializer):
    fichiers = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    localisation = serializers.JSONField()

    class Meta:
        model = ActiviteCommunautaire
        fields = ['id', 'titre', 'description', 'date_debut', 'date_fin','organisateur','commune', 'localisation', 'date_debut_inscriptions', 'date_fin_inscriptions', 'inscriptions_actives', 'nombre_participants_max', 'fichiers']
        read_only_fields = ['organisateur', 'commune']

    def create(self, validated_data):
        fichiers = validated_data.pop('fichiers', [])
        organisateur = self.context['request'].user
        localisation_data = validated_data.pop('localisation')
        validated_data.pop('inscriptions_actives', None)
        localisation = Localisation.objects.create(**localisation_data)
        try:
            organisateur = Personne.objects.get(compte_ptr_id=organisateur.id)
            commune = organisateur.commune
        except Personne.DoesNotExist:
            raise serializers.ValidationError("Utilisateur invalide")
        activiteCommunautaire = ActiviteCommunautaire.objects.create(
            **validated_data,
            organisateur=organisateur,
            inscriptions_actives=True,
            commune=commune,
            localisation=localisation
    
        )
        for fichier in fichiers:
            fichier_obj = Fichier.objects.create(
                nomFichier=fichier.name,
                poidFichier=f"{fichier.size / (1024 * 1024):.2f} MB",
                cheminFichier=fichier,
                context='activite_communautaire'
            )
            activiteCommunautaire.fichiers.add(fichier_obj)
        return activiteCommunautaire





class ActiviteCommunautaireListSerializer(serializers.ModelSerializer):
    nombre_participants_actuels = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    organisateur = PersonneListSerializer()
    localisation = LocalisationSerializer()
    fichiers = FichierSerializer(many=True, read_only=True)
    est_inscrit = serializers.SerializerMethodField()
   

    class Meta:
            model = ActiviteCommunautaire
            fields = ['id', 'titre',
                       'description','est_inscrit' ,
                       'date_debut', 'date_fin',
                       'organisateur', 'participants',
                       'localisation', 'date_debut_inscriptions',
                         'date_fin_inscriptions', 'inscriptions_actives',
                           'nombre_participants_max', 'fichiers',
                           'nombre_participants_actuels']
           
    def get_nombre_participants_actuels(self, obj):
        return obj.participants.count()

    def get_participants(self, obj):
        participants = obj.participants.all()
        print(f"Nombre de participants pour l'activité {obj.id}: {participants.count()}")
        print(f"Participants: {list(participants.values('id', 'nom', 'prenom'))}")
        return PersonneListSerializer(participants, many=True, context=self.context).data
    
    def get_est_inscrit(self, obj):
        user = self.context['request'].user
        if user.is_authenticated and hasattr(user, 'personne'):
            return obj.participants.filter(id=user.personne.id).exists()
        return False


