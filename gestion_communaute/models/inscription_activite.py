from django.db import models
from gestion_communaute.models.activite_communautaire import ActiviteCommunautaire
from gestion_comptes.models.personne import Personne

class Inscription(models.Model):
    activite = models.ForeignKey(ActiviteCommunautaire, on_delete=models.CASCADE, related_name='inscriptions')
    participant = models.ForeignKey(Personne, on_delete=models.CASCADE, related_name='activites_inscrites')
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('activite', 'participant')