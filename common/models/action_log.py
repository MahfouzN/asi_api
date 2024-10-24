from django.db import models

from authentification.models import Compte

class ActionLog(models.Model):
    user = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='actions')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.telephone} - {self.action} - {self.timestamp}"