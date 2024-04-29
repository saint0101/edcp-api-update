"""
Vue pour l'utilisateur API.
"""
# Importations nécessaires depuis le framework Django REST
from rest_framework import generics, authentication, permissions
# Importation du sérialiseur d'utilisateur
from user.serializers import UserSerializer
# Importation de la vue pour obtenir le jeton d'authentification
from rest_framework.authtoken.views import ObtainAuthToken
# Importation du sérialiseur de jeton d'authentification
from user.serializers import AuthTokenSerializer
# Importation des paramètres par défaut du framework REST
from rest_framework.settings import api_settings

# Utilisation du sérialiseur de jeton d'authentification
serializer_class = AuthTokenSerializer
# Utilisation des classes de rendu par défaut du framework REST
renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# Vue pour créer un nouvel utilisateur
class CreateUserView(generics.CreateAPIView):
    """Crée un nouvel utilisateur dans le système."""
    serializer_class = UserSerializer

# Vue pour créer un jeton d'authentification
class CreateTokenView(ObtainAuthToken):
    """ serialiser les champs pour la creation du token """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# Vue pour gérer l'utilisateur authentifié
class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Gestion de l'authentification de l'utilisateur."""

    serializer_class = UserSerializer  # Définit le sérialiseur pour la vue
    authentication_classes = [authentication.TokenAuthentication]  # Définit les classes d'authentification utilisées
    permission_classes = [permissions.IsAuthenticated]  # Définit les permissions requises pour accéder à la vue

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
