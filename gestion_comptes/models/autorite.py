
from django.db import models
from authentification.models import Compte
from gestion_comptes.models.type_autorite import TypeAutorite
from django.utils.translation import gettext_lazy as _

class AutoriteCompetente(Compte):
    nom = models.CharField(max_length=255)
    type_autorite = models.ForeignKey(TypeAutorite, on_delete=models.PROTECT, related_name='autorites')
    zone_competence = models.ForeignKey('Commune',on_delete=models.PROTECT,  related_name='autorites')

    class Meta:
        verbose_name = _("Autorité compétente")
        verbose_name_plural = _("Autorités compétentes")


