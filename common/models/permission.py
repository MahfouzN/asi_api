from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist

class IsSuperAdminOrAdminForOwnCommune(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superadmin:
            return True
        if request.user.role == 'administrateur':
            try:
                return request.user.personne.commune is not None
            except ObjectDoesNotExist:
                return False
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superadmin:
            return True
        if request.user.role == 'administrateur':
            try:
                if hasattr(obj, 'commune'):
                    return obj.commune == request.user.personne.commune
                if hasattr(obj, 'zone_competence'):
                    return obj.zone_competence == request.user.personne.commune
            except ObjectDoesNotExist:
                return False
        return False