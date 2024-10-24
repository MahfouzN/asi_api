from django.db import models
from django.utils import timezone
from common.models.fichier import Fichier
from common.models.localisation import Localisation
from gestion_comptes.models.commune import Commune
from gestion_comptes.models.personne import Personne 


class ActiviteCommunautaire(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    organisateur = models.ForeignKey(Personne, on_delete=models.CASCADE, related_name='activites_organisees')
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='activites')
    localisation = models.ForeignKey(Localisation, on_delete=models.SET_NULL, null=True,related_name='localisationActivite')
    date_debut_inscriptions = models.DateTimeField()
    date_fin_inscriptions = models.DateTimeField()
    inscriptions_actives = models.BooleanField(default=True)
    nombre_participants_max = models.PositiveIntegerField()
    participants = models.ManyToManyField(Personne, blank=True,through='Inscription', related_name='activites_participes')
    fichiers = models.ManyToManyField(Fichier, blank=True)

    def __str__(self):
        return self.titre

    @property
    def nombre_participants_actuels(self):
        return self.participants.count()

    def est_complet(self):
        return self.nombre_participants_actuels >= self.nombre_participants_max

    def peut_s_inscrire(self):
        now = timezone.now()
        return (
            self.inscriptions_actives and
            self.date_debut_inscriptions <= now <= self.date_fin_inscriptions and
            self.participants.count() < self.nombre_participants_max
        )