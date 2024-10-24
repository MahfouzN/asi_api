import os
from uuid import uuid4
from django.db import models

def unique_file_path(instance, filename):
    ext = filename.split('.')[-1]
    context = instance.context if hasattr(instance, 'context') else 'default'
    filename = f"{uuid4()}.{ext}"
    return os.path.join('uploads', instance.get_file_type(), context, filename)

class Fichier(models.Model):
    idFichier = models.AutoField(primary_key=True)
    nomFichier = models.CharField(max_length=255)
    poidFichier = models.CharField(max_length=255)
    dateAjoutFichier = models.DateTimeField(auto_now_add=True)
    cheminFichier = models.FileField(upload_to=unique_file_path)
    typeFichier = models.CharField(max_length=20, blank=True)  # Optionnel, sera déterminé automatiquement
    context = models.CharField(max_length=50, default='default')  # Champ context

    def save(self, *args, **kwargs):
        # Déterminer le type de fichier si ce n'est pas défini
        if not self.typeFichier:
            self.typeFichier = self.get_file_type()
        super().save(*args, **kwargs)

    def get_file_type(self):
        # Déduire le type de fichier à partir de l'extension du fichier
        if self.cheminFichier:
            ext = self.cheminFichier.name.split('.')[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'gif']:
                return 'image'
            elif ext in ['mp4', 'mov', 'avi', 'mkv']:
                return 'video'
            else:
                return 'autres'
        return 'autres'

    def __str__(self):
        return self.nomFichier