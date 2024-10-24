from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from common.models.fichier import Fichier
from gestion_communaute.models.publication import Publication
from gestion_communaute.serializers.publication_citoyen_serilializers import  PublicationListSerializer, PublicationSerializer
from gestion_communaute.serializers.signalement_publication_serializer import SignalementPublicationSerializer
from common.models.action_log import ActionLog
from gestion_comptes.models.autorite import AutoriteCompetente
from utils.api_response import api_response
from django.db.models import Prefetch

class PublicationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Vérifier si l'utilisateur a le rôle d'autorité
        is_authority = user.role == 'autorite'
        
        if is_authority:
            # Si c'est une autorité, retourner toutes les publications sans filtre
            publications = Publication.objects.all()
        else:
            # Si ce n'est pas une autorité, appliquer les filtres
            publications = Publication.objects.filter(est_active=True, est_publie=True)
        
        return publications.order_by('-date_creation')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'mes_publications']:
            return PublicationListSerializer
        return PublicationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response("0000", "Liste des publications récupérée avec succès", serializer.data)
    
    @action(detail=False, methods=['get'])
    def mes_publications(self, request):
        user = request.user
        publications = Publication.objects.filter(auteur=user).order_by('-date_creation')
        
        page = self.paginate_queryset(publications)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(publications, many=True)
        return api_response("0000", "Vos publications récupérées avec succès", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response("0000", "Détails de la publication récupérés avec succès", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action="Création de publication",
                details=f"Publication '{instance.titre}' créée"
            )
            return api_response("0000", "Publication créée avec succès", status.HTTP_201_CREATED)
        return api_response("0002", "Erreur lors de la création de la publication", serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            updated_instance = serializer.save()
            ActionLog.objects.create(
                user=request.user,
                action="Modification de publication",
                details=f"Publication '{updated_instance.titre}' modifiée"
            )
            return api_response("0000", "Publication modifiée avec succès", serializer.data)
        return api_response("0002", "Erreur lors de la modification de la publication", serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        titre_publication = instance.titre
        instance.delete()
        ActionLog.objects.create(
            user=request.user,
            action="Suppression de publication",
            details=f"Publication '{titre_publication}' supprimée"
        )
        return api_response("0000", "Publication supprimée avec succès")

    @action(detail=True, methods=['post'])
    def toggle_like(self, request, pk=None):
        publication = self.get_object()
        if request.user in publication.likes.all():
            publication.likes.remove(request.user)
            action = 'retiré'
        else:
            publication.likes.add(request.user)
            action = 'ajouté'
        ActionLog.objects.create(
            user=request.user,
            action=f"Like {action}",
            details=f"Like {action} sur la publication '{publication.titre}'"
        )
        return api_response("0000", f"Like {action} avec succès", {'nombre_likes': publication.likes.count()})

    @action(detail=True, methods=['post'])
    def signaler(self, request, pk=None):
        publication = self.get_object()
        serializer = SignalementPublicationSerializer(data=request.data)
        if serializer.is_valid():
            signalement = serializer.save(publication=publication, signaleur=request.user)
            ActionLog.objects.create(
                user=request.user,
                action="Signalement de publication",
                details=f"Publication '{publication.titre}' signalée"
            )
            return api_response("0000", "Publication signalée avec succès", serializer.data, status.HTTP_201_CREATED)
        return api_response("0002", "Erreur lors du signalement de la publication", serializer.errors, status.HTTP_400_BAD_REQUEST)