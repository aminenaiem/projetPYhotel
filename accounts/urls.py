from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('login/', views.connexion, name='connexion'),
    path('logout/', views.deconnexion, name='deconnexion'),
    path('profil/', views.profil, name='profil'),
]
