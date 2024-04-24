"""
Tests pour les modifications de l'admin Django.
"""
from django.test import TestCase  # Importe la classe TestCase du module django.test pour les tests unitaires
from django.contrib.auth import get_user_model  # Importe la fonction get_user_model pour obtenir le modèle d'utilisateur personnalisé
from django.urls import reverse  # Importe la fonction reverse pour la résolution d'URL
from django.test import Client  # Importe la classe Client du module django.test pour les tests de requête


class AdminSiteTests(TestCase):
    """Tests pour l'admin Django."""

    def setUp(self):
        """Crée un utilisateur et un client."""
        self.client = Client()  # Crée un client pour effectuer les requêtes
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',  # Crée un superutilisateur avec l'adresse e-mail et le mot de passe fournis
            password='testpass123',
        )
        self.client.force_login(self.admin_user)  # Connecte le client en utilisant les informations de l'admin
        self.user = get_user_model().objects.create_user(
            email='user@example.com',  # Crée un utilisateur avec l'adresse e-mail, le mot de passe et le nom fournis
            password='testpass123',
            name='Test User'
        )

    def test_users_lists(self):
        """Vérifie que les utilisateurs sont répertoriés sur la page."""
        url = reverse('admin:edcp_apirest_user_changelist')  # Récupère l'URL de la liste des utilisateurs dans l'admin
        res = self.client.get(url)  # Effectue une requête GET à l'URL de la liste des utilisateurs

        # Vérifie que la réponse contient le nom et l'e-mail de l'utilisateur
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)


    def test_edit_user_page(self):
        """Vérifie que les utilisateurs sont répertoriés sur la page."""

        url = reverse('admin:edcp_apirest_user_change', args=[self.user.id])  # Récupère l'URL de la liste des utilisateurs dans l'admin
        res = self.client.get(url) # Effectue une requête GET à l'URL de la liste des utilisateurs

        # Vérifie que la réponse contient le nom et l'e-mail de l'utilisateur
        self.assertEqual(res.status_code, 200)


    def test_create_user_page(self):
        """ Creation des utilisateur sur la page """
        url = reverse('admin:edcp_apirest_user_add')
        res = self.client.get(url)

        # Vérifie que la réponse contient l'utilisateur creer
        self.assertEqual(res.status_code, 200)