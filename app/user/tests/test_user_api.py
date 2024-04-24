"""
Test de l'API utilisateur.
"""

from django.urls import reverse  # Importe la fonction reverse pour obtenir l'URL d'une vue par son nom
from django.test import TestCase  # Importe la classe TestCase pour les tests Django
from django.contrib.auth import get_user_model  # Importe la fonction get_user_model pour obtenir le modèle utilisateur

from rest_framework.test import APIClient  # Importe la classe APIClient pour les tests de l'API REST
from rest_framework import status  # Importe les constantes de statut HTTP

# URL pour créer un utilisateur
CREATE_USER_URL = reverse('user:create')


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
