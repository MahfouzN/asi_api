import random
import string
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from authentification.serializers.compte_serializer import CompteListSerializer
from common.models.action_log import ActionLog
from rest_framework import viewsets, permissions, status
from gestion_comptes.serializers.autorite_serializers import AutoriteCompetenteSerializer
from gestion_comptes.serializers.personne_serializers import PersonneSerializer
from authentification.views.compte_view import *
from utils.api_response import api_response

class AdminCompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            if self.request.data.get('role') == 'autorite':
                return AutoriteCompetenteSerializer
            elif self.request.data.get('role') in ['citoyen', 'responsable', 'administrateur']:
                return PersonneSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if request.data.get('role') == 'autorite':
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        else:
            password = request.data.get('password')
        
        if not password:
            return api_response("0002", "Le mot de passe est requis", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_password(password)
        except ValidationError as e:
            return api_response("0002", "Erreur de validation du mot de passe", e.messages, status=status.HTTP_400_BAD_REQUEST)
        
        compte = serializer.save(password=password)
        ActionLog.objects.create(
            user=request.user,
            action="Création de compte",
            details=f"Compte créé pour {compte.telephone} avec le rôle {compte.role}"
        )
        response_data = serializer.data
        if request.data.get('role') == 'autorite':
            response_data['generated_password'] = password
        return api_response("0000", "Compte créé avec succès", response_data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        compte = self.get_object()
        compte.is_active = not compte.is_active
        compte.save()
        ActionLog.objects.create(
            user=request.user,
            action=f"{'Activation' if compte.is_active else 'Désactivation'} de compte",
            details=f"Compte {compte.telephone} {'activé' if compte.is_active else 'désactivé'}"
        )
        return api_response("0000", "Statut du compte mis à jour", {'is_active': compte.is_active})

    @transaction.atomic
    @action(detail=True, methods=['post'])
    def change_role(self, request, pk=None):
        compte = self.get_object()
        new_role = request.data.get('role')
        
        if new_role not in dict(Compte.ROLE_CHOICES):
            return api_response("0002", "Rôle invalide", status=status.HTTP_400_BAD_REQUEST)
        
        old_role = compte.role
        
        # Vérification des règles de changement de rôle
        if old_role == 'autorite' or new_role == 'autorite':
            return api_response("0002", "Impossible de changer le rôle d'une autorité ou en autorité", status=status.HTTP_400_BAD_REQUEST)
        
        if old_role not in ['citoyen', 'responsable', 'administrateur'] or new_role not in ['citoyen', 'responsable', 'administrateur']:
            return api_response("0002", "Changement de rôle non autorisé", status=status.HTTP_400_BAD_REQUEST)
        
        # Gestion du rôle administrateur
        if new_role == 'administrateur':
            # Vérifier si c'est le premier administrateur (superadmin)
            if not Compte.objects.filter(is_superadmin=True).exists():
                compte.is_superadmin = True
            else:
                # Vérifier si l'utilisateur a une commune associée
                try:
                    personne = Personne.objects.get(compte_ptr_id=compte.id)
                    if not personne.commune:
                        return api_response("0002", "Un administrateur local doit être associé à une commune", status=status.HTTP_400_BAD_REQUEST)
                except Personne.DoesNotExist:
                    return api_response("0002", "Impossible de trouver les informations de la personne", status=status.HTTP_400_BAD_REQUEST)

        # Mise à jour du rôle et des permissions
        compte.role = new_role
        compte.is_staff = (new_role == 'administrateur')
        compte.save()
        
        # Création du log d'action
        ActionLog.objects.create(
            user=request.user,
            action="Changement de rôle",
            details=f"Rôle du compte {compte.telephone} changé de {old_role} à {new_role}"
        )
        
        return api_response("0000", "Rôle mis à jour avec succès", {
            'new_role': new_role, 
            'is_staff': compte.is_staff,
            'is_superadmin': compte.is_superadmin
        })

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CompteListSerializer(queryset, many=True)
        return api_response("0000", "Liste des comptes récupérée avec succès", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response("0000", "Détails du compte récupérés avec succès", serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        ActionLog.objects.create(
            user=request.user,
            action="Modification de compte",
            details=f"Compte {instance.telephone} modifié"
        )
        return api_response("0000", "Compte mis à jour avec succès", serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        telephone = instance.telephone
        self.perform_destroy(instance)
        ActionLog.objects.create(
            user=request.user,
            action="Suppression de compte",
            details=f"Compte {telephone} supprimé"
        )
        return api_response("0000", "Compte supprimé avec succès")