# Generated by Django 4.2 on 2024-10-20 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('gestion_comptes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiviteCommunautaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date_debut', models.DateTimeField()),
                ('date_fin', models.DateTimeField()),
                ('date_debut_inscriptions', models.DateTimeField()),
                ('date_fin_inscriptions', models.DateTimeField()),
                ('inscriptions_actives', models.BooleanField(default=True)),
                ('nombre_participants_max', models.PositiveIntegerField()),
                ('commune', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activites', to='gestion_comptes.commune')),
                ('fichiers', models.ManyToManyField(blank=True, to='common.fichier')),
                ('localisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='localisationActivite', to='common.localisation')),
                ('organisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activites_organisees', to='gestion_comptes.personne')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_mise_a_jour', models.DateTimeField(auto_now=True)),
                ('est_publie', models.BooleanField(default=False)),
                ('est_active', models.BooleanField(default=True)),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s', to=settings.AUTH_USER_MODEL)),
                ('commune', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s', to='gestion_comptes.commune')),
                ('fichiers', models.ManyToManyField(blank=True, related_name='publications', to='common.fichier')),
            ],
        ),
        migrations.CreateModel(
            name='SignalementPublication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raison', models.TextField()),
                ('date_signalement', models.DateTimeField(auto_now_add=True)),
                ('est_traite', models.BooleanField(default=False)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signalements', to='gestion_communaute.publication')),
                ('signaleur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signalements_effectues', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_inscription', models.DateTimeField(auto_now_add=True)),
                ('activite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscriptions', to='gestion_communaute.activitecommunautaire')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activites_inscrites', to='gestion_comptes.personne')),
            ],
            options={
                'unique_together': {('activite', 'participant')},
            },
        ),
        migrations.CreateModel(
            name='Annonce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annonce_image', to='common.fichier')),
                ('visible_dans_commune', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_comptes.commune')),
            ],
        ),
        migrations.AddField(
            model_name='activitecommunautaire',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='activites_participes', through='gestion_communaute.Inscription', to='gestion_comptes.personne'),
        ),
    ]
