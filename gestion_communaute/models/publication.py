from django.db import models
from authentification.models import Compte
from common.models.fichier import Fichier
from gestion_comptes.models.commune import Commune


class Publication(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    auteur = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s')
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s')
    fichiers = models.ManyToManyField(Fichier, related_name='publications', blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    est_publie = models.BooleanField(default=False)
    est_active = models.BooleanField(default=True)
   