from django.db import models
from common.models.localisation import Localisation
from gestion_comptes.models.personne import Personne



class Commune(models.Model):
    numOrdre=models.IntegerField(null=True)
    nomCommune=models.CharField(max_length=255)
    maire = models.OneToOneField(Personne, on_delete=models.SET_NULL, null=True, related_name='commune_dirigee')

    localisationCommune = models.ForeignKey(Localisation ,on_delete=models.SET_NULL,null=True, related_name='localisationCommune')
    def __str__(self):
        return self.nomCommune