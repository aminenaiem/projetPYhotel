from django.db import models
from rooms.models import Chambre
from clients.models import Client

class Reservation(models.Model):
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE, verbose_name="Chambre")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    date_checkin = models.DateField(verbose_name="Date d'arrivée")
    date_checkout = models.DateField(verbose_name="Date de départ")
    prix_total = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Prix total (MAD)", default=0
    )

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-date_checkin']

    def __str__(self):
        return f"Rés. #{self.pk} – {self.client} | {self.chambre}"

    @property
    def nb_nuits(self):
        if self.date_checkin and self.date_checkout:
            return (self.date_checkout - self.date_checkin).days
        return 0

    def save(self, *args, **kwargs):
        if self.chambre_id and self.date_checkin and self.date_checkout:
            self.prix_total = self.chambre.prix * self.nb_nuits
        super().save(*args, **kwargs)
