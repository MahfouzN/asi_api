from django.db import models
from common.models.fichier import Fichier
from .incident import Incident

class FichierIncident(models.Model):
    fichier = models.ForeignKey(Fichier, on_delete=models.CASCADE)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='fichier_incidents')

    def __str__(self):
        return f"Fichier pour {self.incident}"