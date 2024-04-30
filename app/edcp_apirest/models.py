"""
    Model de la base de données
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    """Gestionnaire pour les utilisateurs."""

    def create_user(self, email, password=None, **extra_fields):
        """Crée, enregistre et retourne un nouvel utilisateur."""
        if not email:
            raise ValueError("L'utilisateur doit avoire une adresse email.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password):
        """Crée et enregistre un superutilisateur avec les informations fournies."""

        user = self.create_user(email, password)  # Crée un nouvel utilisateur avec l'email et le mot de passe fournis
        user.is_staff = True  # Définit l'utilisateur comme membre du personnel
        user.is_superuser = True  # Définit l'utilisateur comme superutilisateur
        user.save(using=self._db)  # Enregistre l'utilisateur dans la base de données

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Utilisateur dans le système."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # instance de la table utilisateur
    objects = UserManager()

    # Champ d'identification de l'utilisateur (par défaut, 'username' ou 'email')
    USERNAME_FIELD = 'email'