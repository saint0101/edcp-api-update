"""
Vue pour l'utilisateur API.
"""
from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Crée un nouvel utilisateur dans le système."""
    serializer_class = UserSerializer
