from rest_framework import viewsets ,status
from rest_framework.response import Response
from rest_framework.decorators import action
from authentification.models import *
from rest_framework.response import Response
from rest_framework.decorators import action
from authentification.serializers.change_password_serializer import ChangePasswordSerializer
from authentification.serializers.compte_detail_serializer import CompteDetailSerializer
from authentification.serializers.compte_serializer import  CompteSerializer
from rest_framework import viewsets, permissions
from common.models.action_log import ActionLog
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from datetime import datetime
from pytz import UTC
from django.contrib.auth import update_session_auth_hash
from gestion_comptes.models.autorite import AutoriteCompetente
from gestion_comptes.models.personne import Personne
from gestion_comptes.serializers.autorite_serializers import AutoriteCompetenteSerializer
from gestion_comptes.serializers.personne_serializers import PersonneSerializer
from gestion_comptes.serializers.type_autorite_serializers import TypeAutoriteSerializer
from utils.api_response import api_response

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = Compte.objects.get(telephone=request.data['telephone'])
            
            # Log the action
            ActionLog.objects.create(
                user=user,
                action="Connexion",
                details=f"Connexion réussie pour {user.telephone}"
            )
            access_token = AccessToken(response.data['access'])
            refresh_token = RefreshToken(response.data['refresh'])
            # Add additional user information to the response
            access_expiration = datetime.fromtimestamp(access_token['exp'], UTC).isoformat()
            additional_data = {
                'photo': user.photo.cheminFichier.url if user.photo else None,
                'email': user.email,
                'expiration': access_expiration,
                'status_code': response.status_code,
            }
            
            # Merge the additional data with the token data
            response.data.update(additional_data)
        
        return response
    



class CompteDetailView(viewsets.ReadOnlyModelViewSet):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Compte.objects.filter(id=self.request.user.id)

    def get_specific_instance(self, compte):
        try:
            return Personne.objects.get(compte_ptr_id=compte.id)
        except Personne.DoesNotExist:
            try:
                return AutoriteCompetente.objects.get(compte_ptr_id=compte.id)
            except AutoriteCompetente.DoesNotExist:
                return None

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        specific_instance = self.get_specific_instance(user)

        data = {
            'id': user.id,
            'telephone': user.telephone,
            'email': user.email,
            'username': user.username,
            'role': user.role,
            'photo': user.photo.cheminFichier.url if user.photo else None,
        }

        if isinstance(specific_instance, Personne):
            data.update({
                'nom': specific_instance.nom,
                'prenom': specific_instance.prenom,
                'commune': specific_instance.commune.id if specific_instance.commune else None,
            })
        elif isinstance(specific_instance, AutoriteCompetente):
            data.update({
                'type_autorite': TypeAutoriteSerializer(specific_instance.type_autorite).data if specific_instance.type_autorite else None,
                'zone_competence': specific_instance.zone_competence.id if specific_instance.zone_competence else None,
            })

        ActionLog.objects.create(
            user=request.user,
            action="Consultation du profil",
            details=f"L'utilisateur a consulté son profil"
        )

        return api_response("0000", "Détails du compte récupérés avec succès", data)
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return api_response("0002", "Ancien mot de passe incorrect")
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)  # Important pour maintenir la session de l'utilisateur
            
            ActionLog.objects.create(
                user=user,
                action="Changement de mot de passe",
                details="L'utilisateur a changé son mot de passe"
            )
            
            return api_response("0000", "Mot de passe mis à jour avec succès")
        return api_response("0002", "Erreur lors de la mise à jour du mot de passe", serializer.errors)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response("0000", "Liste des comptes récupérée avec succès", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response("0000", "Détails du compte récupérés avec succès", serializer.data)