from django.db import models
from common.models.fichier import Fichier
from gestion_comptes.models.personne import Personne
from gestion_comptes.models.commune import Commune
from common.models.localisation import Localisation
from .type_incident import TypeIncident

class StatutTraitement(models.TextChoices):
    EN_ATTENTE = 'EN_ATTENTE', 'En attente'
    EN_TRAITEMENT = 'EN_TRAITEMENT', 'En traitement'
    TRAITE = 'TRAITE', 'Traité'
    REJETE = 'REJETE', 'Rejeté'

class Incident(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_incident = models.DateTimeField()
    type_incident = models.ForeignKey(TypeIncident, on_delete=models.CASCADE)
    signaleur = models.ForeignKey(Personne, on_delete=models.CASCADE, related_name='incidents_signales')
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='incidents')
    localisation = models.ForeignKey(Localisation, on_delete=models.SET_NULL, null=True)
    fichiers = models.ManyToManyField(Fichier, through='FichierIncident', related_name='incidents')
    statut = models.CharField(max_length=20, choices=StatutTraitement.choices, default=StatutTraitement.EN_ATTENTE)
    autorite_en_charge = models.ForeignKey('gestion_comptes.AutoriteCompetente', 
                                           on_delete=models.SET_NULL, 
                                           null=True, 
                                           related_name='incidents_en_charge')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.titre} - {self.commune}"