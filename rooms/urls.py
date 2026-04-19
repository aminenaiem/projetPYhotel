from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.liste_chambres, name='liste'),
    path('<int:pk>/', views.detail_chambre, name='detail'),
    path('ajouter/', views.ajouter_chambre, name='ajouter'),
    path('<int:pk>/modifier/', views.modifier_chambre, name='modifier'),
    path('<int:pk>/supprimer/', views.supprimer_chambre, name='supprimer'),
]
