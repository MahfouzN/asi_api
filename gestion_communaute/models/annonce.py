from django.db import models
from common.models.fichier import Fichier  
from gestion_comptes.models.commune import Commune  

class Annonce(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ForeignKey(Fichier, on_delete=models.CASCADE, related_name='annonce_image')  
    date_creation = models.DateTimeField(auto_now_add=True)  
    is_active = models.BooleanField(default=True) 
    visible_dans_commune = models.ForeignKey(Commune, null=True, blank=True, on_delete=models.SET_NULL) 

    def __str__(self):
        return self.nom