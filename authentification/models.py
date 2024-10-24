from django.db import models
from common.models.fichier import Fichier
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_user(self, telephone, email, username, password=None, **extra_fields):
        if not telephone:
            raise ValueError(_('Le numéro de téléphone est obligatoire'))
        if not username:
            raise ValueError(_('Le nom d’utilisateur est obligatoire'))
        email = self.normalize_email(email)
        user = self.model(telephone=telephone, email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telephone, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_superadmin', True)
        extra_fields.setdefault('role', 'administrateur')
        return self.create_user(telephone, email, username, password, **extra_fields)


class Compte(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('citoyen', 'Citoyen'),
        ('responsable', 'Responsable communautaire'),
        ('administrateur', 'Administrateur'),
        ('autorite', 'Autorité compétente'),
    ]

    telephone = models.CharField(_("téléphone"), max_length=150, unique=True)
    email = models.EmailField(_("adresse e-mail"), unique=True)
    username = models.CharField(_("nom d'utilisateur"), max_length=150, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    photo = models.ForeignKey(Fichier, on_delete=models.SET_NULL, null=True, related_name='compte_photo')

    objects = CustomAccountManager()

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['email', 'username', 'role']

    def __str__(self):
        return f"{self.telephone} ({self.get_role_display()})"
