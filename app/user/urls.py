# Importation des modules nécessaires
from django.urls import path

# Importation des vues de l'utilisateur
from user import views

# Nom de l'application
app_name = 'user'

# Définition des URL
urlpatterns = [
    # URL pour créer un nouvel utilisateur
    path('create/', views.CreateUserView.as_view(), name='create'),
]
