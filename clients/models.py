"""
Modèle Client – informations sur les clients de l'hôtel
"""
from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    # Lien optionnel vers un compte utilisateur Django
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='client'
    )
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    adresse = models.TextField(blank=True, verbose_name="Adresse")
    cin = models.CharField(
        max_length=20, blank=True,
        verbose_name="CIN / Passeport"
    )
    nationalite = models.CharField(
        max_length=50, blank=True,
        verbose_name="Nationalité"
    )
    date_naissance = models.DateField(
        null=True, blank=True,
        verbose_name="Date de naissance"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

    @property
    def nb_reservations(self):
        return self.reservation_set.count()
