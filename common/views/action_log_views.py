from rest_framework import viewsets, permissions

from common.models.action_log import ActionLog
from common.models.permission import IsSuperAdminOrAdminForOwnCommune
from common.serializers.action_log_serializers import ActionLogSerializer


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class ActionLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActionLog.objects.all().order_by('-timestamp')
    serializer_class = ActionLogSerializer
    permission_classes = [permissions.IsAuthenticated & IsSuperAdminOrAdminForOwnCommune]

    def get_queryset(self):
        return super().get_queryset()