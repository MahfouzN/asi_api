from django.db import models


class Localisation(models.Model):
    idLocalisation = models.AutoField(primary_key=True)
    longitude=models.FloatField(default=0)
    latitude= models.FloatField(default=0)
    limiteNord= models.CharField(max_length=255,blank=True,null=True)
    limiteSud= models.CharField(max_length=255,blank=True,null=True)
    limiteEst= models.CharField(max_length=255,blank=True,null=True)
    limiteOuest= models.CharField(max_length=255,blank=True,null=True)
    nomDuLieu= models.CharField(max_length=255,blank=True,null=True)
    description= models.TextField()

    