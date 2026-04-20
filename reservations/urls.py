from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.liste_reservations, name='liste'),
    path('<int:pk>/', views.detail_reservation, name='detail'),
    path('ajouter/', views.ajouter_reservation, name='ajouter'),
    path('<int:pk>/modifier/', views.modifier_reservation, name='modifier'),
    path('<int:pk>/statut/', views.changer_statut, name='statut'),
    path('<int:pk>/supprimer/', views.supprimer_reservation, name='supprimer'),
]
