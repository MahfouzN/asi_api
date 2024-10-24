# Generated by Django 4.2 on 2024-10-20 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('authentification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numOrdre', models.IntegerField(null=True)),
                ('nomCommune', models.CharField(max_length=255)),
                ('localisationCommune', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='localisationCommune', to='common.localisation')),
            ],
        ),
        migrations.CreateModel(
            name='TypeAutorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('compte_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
                ('commune', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='personnes', to='gestion_comptes.commune')),
            ],
            options={
                'verbose_name': 'Personne',
                'verbose_name_plural': 'Personnes',
            },
            bases=('authentification.compte',),
        ),
        migrations.AddField(
            model_name='commune',
            name='maire',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commune_dirigee', to='gestion_comptes.personne'),
        ),
        migrations.CreateModel(
            name='AutoriteCompetente',
            fields=[
                ('compte_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nom', models.CharField(max_length=255)),
                ('type_autorite', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='autorites', to='gestion_comptes.typeautorite')),
                ('zone_competence', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='autorites', to='gestion_comptes.commune')),
            ],
            options={
                'verbose_name': 'Autorité compétente',
                'verbose_name_plural': 'Autorités compétentes',
            },
            bases=('authentification.compte',),
        ),
    ]
