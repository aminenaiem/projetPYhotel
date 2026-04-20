"""
Modèle Chambre pour la gestion des chambres d'hôtel
"""
from django.db import models


class Chambre(models.Model):
    TYPE_CHOICES = [
        ('simple', 'Simple'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('deluxe', 'Deluxe'),
        ('familiale', 'Familiale'),
    ]

    numero = models.CharField(max_length=10, unique=True, verbose_name="Numéro")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix / nuit (MAD)")
    disponible = models.BooleanField(default=True, verbose_name="Disponible")
    description = models.TextField(blank=True, verbose_name="Description")
    capacite = models.PositiveIntegerField(default=2, verbose_name="Capacité (personnes)")
    etage = models.PositiveIntegerField(default=1, verbose_name="Étage")
    superficie = models.PositiveIntegerField(default=25, verbose_name="Superficie (m²)")
    image = models.ImageField(upload_to='chambres/', blank=True, null=True, verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Chambre"
        verbose_name_plural = "Chambres"
        ordering = ['numero']

    def __str__(self):
        return f"Chambre {self.numero} – {self.get_type_display()}"

    @property
    def statut_badge(self):
        return 'success' if self.disponible else 'danger'

    @property
    def statut_label(self):
        return 'Disponible' if self.disponible else 'Occupée'
