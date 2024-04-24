"""
Personnalisation de l'administration Django.
"""
from django.contrib import admin  # noqa
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# Importe les modèles ici
from edcp_apirest import models

class UserAdmin(BaseUserAdmin):
    """Définit les pages d'administration pour les utilisateurs."""
    ordering = ['id']  # Ordonne les utilisateurs par ID
    list_display = ['email', 'name']  # Affiche les utilisateurs par e-mail et nom

    # Éditer l'utilisateur
    fieldsets = (
        (None, {'fields': ('email', "password")}),  # Informations de connexion
        (
            _('Permissions'),  # Titre pour les champs de permission
            {
                'fields': (
                    'is_active',    # Active ou désactive le compte
                    'is_staff',     # Accorde l'accès au site d'administration
                    'is_superuser', # Accorde tous les accès
                )
            }
        ),
        (_('Dates importantes'), {'fields': ('last_login',)}),  # Date de dernière connexion
    )
    readonly_fields = ['last_login']  # Affiche la dernière connexion en lecture seule

    # ajoute d'un utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


# Enregistre les modèles ici
admin.site.register(models.User, UserAdmin)
