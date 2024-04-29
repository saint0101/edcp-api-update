"""
Test de l'API utilisateur.
"""

from django.urls import reverse  # Importe la fonction reverse pour obtenir l'URL d'une vue par son nom
from django.test import TestCase  # Importe la classe TestCase pour les tests Django
from django.contrib.auth import get_user_model  # Importe la fonction get_user_model pour obtenir le modèle utilisateur

from rest_framework.test import APIClient  # Importe la classe APIClient pour les tests de l'API REST
from rest_framework import status  # Importe les constantes de statut HTTP

from rest_framework.authtoken.models import Token  # Assurez-vous d'importer Token correctement


# URL pour créer un utilisateur
CREATE_USER_URL = reverse('user:create')

# URL pour créer du token
TOKEN_URL = reverse('user:token')

# URL pour l'utilisateur
ME_URL = reverse('user:me')

def create_user(**params):
    """ Crée un nouvel utilisateur """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ Tests publics de l'API utilisateur. """

    def setUp(self):
        """ Configuration initiale des tests """
        self.client = APIClient()  # Crée un client API pour effectuer les requêtes HTTP

    def test_create_user_success(self):
        """ Création d'un utilisateur avec succès """
        payload = {
            'email': 'test@example.com',  # Email de test
            'password': 'testpass123',  # Mot de passe de test
            'name': 'Test Name',  # Nom de test
        }

        res = self.client.post(CREATE_USER_URL, payload)  # Envoie une requête POST pour créer un utilisateur

        # Vérifie si la création de l'utilisateur a renvoyé le statut HTTP 201 (Créé)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Récupère l'utilisateur nouvellement créé de la base de données
        user = get_user_model().objects.get(email=payload['email'])

        # Vérifie si le mot de passe de l'utilisateur correspond au mot de passe fourni
        self.assertTrue(user.check_password(payload['password']))

        # Vérifie que le mot de passe n'est pas retourné dans les données de la réponse
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """ Test si l'email de l'utilisateur existe, cela doit renvoyer une erreur """
        payload = {
            'email': 'test@example.com',  # Email de test
            'password': 'testpass123',  # Mot de passe de test
            'name': 'Test Name',  # Nom de test
        }
        create_user(**payload)  # Crée un utilisateur avec l'email de test
        res = self.client.post(CREATE_USER_URL, payload)  # Envoie une requête POST pour créer un utilisateur

        # Vérifie si la création de l'utilisateur a renvoyé le statut HTTP 400 (Mauvaise requête)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """ Test la création d'un utilisateur avec un e-mail invalide """
        payload = {
            'email': 'invalid_email',  # Email invalide
            'password': 'testpass123',  # Mot de passe de test
            'name': 'Test Name',  # Nom de test
        }
        res = self.client.post(CREATE_USER_URL, payload)  # Envoie une requête POST pour créer un utilisateur

        # Vérifie si la création de l'utilisateur a renvoyé le statut HTTP 400 (Mauvaise requête)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Vérifie que l'utilisateur n'existe pas
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        """Test la création d'un token pour un utilisateur."""

        # Informations de l'utilisateur de test
        user_details = {
            'email': 'test@example.com',  # Email de test
            'password': 'testpass123',     # Mot de passe de test
            'name': 'Test Name',           # Nom de test
        }

        # Création de l'utilisateur
        create_user(**user_details)

        # Informations pour la génération du token
        payload = {
            'email': user_details['email'],    # Email de l'utilisateur
            'password': user_details['password'],  # Mot de passe de l'utilisateur
        }
        # Envoie une requête POST pour créer le TOKEN
        res = self.client.post(TOKEN_URL, payload)

        # Vérifie la présence du token dans les données de réponse
        self.assertIn('token', res.data)
        # Vérifie le code de statut de la réponse
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_token_bad_credentials(self):
        """Teste le retour d'erreur si les identifiants sont invalides."""
        # Crée un utilisateur avec un bon mot de passe
        create_user(email='test@example.com', password='goodpass')

        # Prépare les données avec des identifiants incorrects
        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        # Vérifie que le token n'est pas dans la réponse et que le statut de la requête est HTTP 400 (Bad Request)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """Teste le retour d'erreur si aucun utilisateur n'est trouvé pour l'e-mail donné."""
        # Prépare les données avec un e-mail qui n'est pas associé à un utilisateur existant
        payload = {'email': 'test@example.com', 'password': 'pass123'}
        res = self.client.post(TOKEN_URL, payload)

        # Vérifie que le token n'est pas dans la réponse et que le statut de la requête est HTTP 400 (Bad Request)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Teste le retour d'erreur si un mot de passe vide est fourni."""
        # Prépare les données avec un mot de passe vide
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        # Vérifie que le token n'est pas dans la réponse et que le statut de la requête est HTTP 400 (Bad Request)
        self.assertNotIn('token', res.data)#
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrieve_user_unauthorized(self):
        """ Tester l'authorisation requi pour l'utilisateur  """

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class  PrivateUserApiTests():
    """ Tester le systeme d'hautentification pour chaque requete """

    def seuUp(self):
        """ les parametres initial des tests """

        self.user = create_user(
            email='test@exemple.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'name': 'Updated name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)