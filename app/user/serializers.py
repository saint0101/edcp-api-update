"""
Serialiseurs pour la vue de l'API utilisateur.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serialiseur pour l'objet utilisateur."""

    class Meta:
        model = get_user_model()  # Récupère le modèle d'utilisateur actif
        fields = ['email', 'password', 'name']  # Champs à inclure dans le sérialiseur
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}  # Options supplémentaires pour les champs

    def create(self, validated_data):
        """Crée et renvoie un utilisateur avec un mot de passe crypté."""
        return get_user_model().objects.create_user(**validated_data)  # Crée un utilisateur avec les données validées
