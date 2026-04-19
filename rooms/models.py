from django.db import models

class Chambre(models.Model):
    numero = models.CharField(max_length=10, unique=True, verbose_name="Numéro")
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix / nuit (MAD)")
    disponible = models.BooleanField(default=True, verbose_name="Disponible")

    class Meta:
        verbose_name = "Chambre"
        verbose_name_plural = "Chambres"
        ordering = ['numero']

    def __str__(self):
        return f"Chambre {self.numero}"

    @property
    def statut_badge(self):
        return 'success' if self.disponible else 'danger'

    @property
    def statut_label(self):
        return 'Disponible' if self.disponible else 'Occupée'
