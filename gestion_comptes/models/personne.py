
from django.db import models
from authentification.models import Compte
from django.utils.translation import gettext_lazy as _

class Personne(Compte):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    commune = models.ForeignKey('Commune', on_delete=models.SET_NULL, null=True, related_name='personnes')

    class Meta:
        verbose_name = _("Personne")
        verbose_name_plural = _("Personnes")
   
