
from gestion_comptes.serializers.autorite_serializers  import *
from authentification.views.compte_view import *
from rest_framework import viewsets, permissions

class AutoriteViewSet(viewsets.ModelViewSet):
    queryset = AutoriteCompetente.objects.all()
    serializer_class = AutoriteCompetenteSerializer
    permission_classes = [permissions.IsAdminUser]