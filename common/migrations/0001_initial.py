# Generated by Django 4.2 on 2024-10-20 18:44

import common.models.fichier
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fichier',
            fields=[
                ('idFichier', models.AutoField(primary_key=True, serialize=False)),
                ('nomFichier', models.CharField(max_length=255)),
                ('poidFichier', models.CharField(max_length=255)),
                ('dateAjoutFichier', models.DateTimeField(auto_now_add=True)),
                ('cheminFichier', models.FileField(upload_to=common.models.fichier.unique_file_path)),
                ('typeFichier', models.CharField(blank=True, max_length=20)),
                ('context', models.CharField(default='default', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Localisation',
            fields=[
                ('idLocalisation', models.AutoField(primary_key=True, serialize=False)),
                ('longitude', models.FloatField(default=0)),
                ('latitude', models.FloatField(default=0)),
                ('limiteNord', models.CharField(blank=True, max_length=255, null=True)),
                ('limiteSud', models.CharField(blank=True, max_length=255, null=True)),
                ('limiteEst', models.CharField(blank=True, max_length=255, null=True)),
                ('limiteOuest', models.CharField(blank=True, max_length=255, null=True)),
                ('nomDuLieu', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('details', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]