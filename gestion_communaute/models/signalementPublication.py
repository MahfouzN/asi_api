from django.db import models
from authentification.models import Compte
from gestion_communaute.models.publication import Publication


class SignalementPublication(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='signalements')
    signaleur = models.ForeignKey(Compte, on_delete=models.CASCADE,  related_name='signalements_effectues')
    raison = models.TextField()
    date_signalement = models.DateTimeField(auto_now_add=True)
    est_traite = models.BooleanField(default=False)

    def __str__(self):
        return f"Signalement de {self.signaleur} pour {self.publication}"