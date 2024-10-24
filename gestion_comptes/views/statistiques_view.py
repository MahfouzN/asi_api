from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Q
from utils.api_response import api_response
from authentification.models import Compte
from gestion_communaute.models.activite_communautaire import ActiviteCommunautaire
from gestion_communaute.models.publication import Publication
from gestion_comptes.models.commune import Commune
from gestion_incidents.models.incident import Incident

class StatistiquesSystemeView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Restreindre l'accès aux administrateurs

    def get(self, request):
        # Nombre d'utilisateurs
        nb_utilisateurs = Compte.objects.count()

        # Nombre de communes
        nb_communes = Commune.objects.count()

        # Nombre d'incidents signalés
        nb_incidents = Incident.objects.count()

        # Nombre de signalements traités
        nb_signalements_traites = Incident.objects.filter(statut='TRAITE').count()

        # Nombre de publications
        nb_publications = Publication.objects.count()

        # Nombre d'activités communautaires
        nb_activites = ActiviteCommunautaire.objects.count()

        # Nombre d'utilisateurs par rôle
        utilisateurs_par_role = Compte.objects.values('role').annotate(count=Count('id'))

        # Nombre d'incidents par statut
        incidents_par_statut = Incident.objects.values('statut').annotate(count=Count('id'))

        # Taux de résolution des incidents
        nb_incidents_resolus = Incident.objects.filter(statut='TRAITE').count()
        taux_resolution = (nb_incidents_resolus / nb_incidents) * 100 if nb_incidents > 0 else 0


        statistiques = {
            "nombre_utilisateurs": nb_utilisateurs,
            "nombre_communes": nb_communes,
            "nombre_incidents": nb_incidents,
            "nombre_signalements_traites": nb_signalements_traites,
            "nombre_publications": nb_publications,
            "nombre_activites": nb_activites,
            "utilisateurs_par_role": list(utilisateurs_par_role),
            "incidents_par_statut": list(incidents_par_statut),
            "taux_resolution_incidents": round(taux_resolution, 2),
           
        }

        return api_response("0000", "Statistiques du système récupérées avec succès", statistiques)