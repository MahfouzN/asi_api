from django.db import models
from gestion_comptes.models.type_autorite import TypeAutorite
from common.models.fichier import Fichier  

class TypeIncident(models.Model):
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True)
    description = models.TextField()
    type_autorite = models.ForeignKey(TypeAutorite, on_delete=models.CASCADE, related_name='types_incidents')
    icon = models.ForeignKey(Fichier, on_delete=models.CASCADE, related_name='type_incident_icon')  
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return self.nom