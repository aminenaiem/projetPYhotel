"""
Modèle Reservation – cœur métier de la gestion hôtelière
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from rooms.models import Chambre
from clients.models import Client


class Reservation(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
        ('terminee', 'Terminée'),
    ]
    STATUT_BADGES = {
        'en_attente': 'warning',
        'confirmee': 'success',
        'annulee': 'danger',
        'terminee': 'secondary',
    }

    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE, verbose_name="Chambre")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        verbose_name="Créée par", related_name='reservations_creees'
    )
    date_checkin = models.DateField(verbose_name="Date d'arrivée")
    date_checkout = models.DateField(verbose_name="Date de départ")
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES,
        default='en_attente', verbose_name="Statut"
    )
    prix_total = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Prix total (MAD)", default=0
    )
    nb_personnes = models.PositiveIntegerField(default=1, verbose_name="Nombre de personnes")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-created_at']

    def __str__(self):
        return f"Rés. #{self.pk} – {self.client} | {self.chambre} | {self.date_checkin}"

    # ── Calculs ──────────────────────────────────────────────────────────────
    @property
    def nb_nuits(self):
        if self.date_checkin and self.date_checkout:
            return (self.date_checkout - self.date_checkin).days
        return 0

    def calculer_prix_total(self):
        return self.chambre.prix * self.nb_nuits

    @property
    def badge_statut(self):
        return self.STATUT_BADGES.get(self.statut, 'secondary')

    # ── Validation métier ─────────────────────────────────────────────────────
    def clean(self):
        if self.date_checkin and self.date_checkout:
            if self.date_checkin >= self.date_checkout:
                raise ValidationError("La date de départ doit être après la date d'arrivée.")
            if self.date_checkin < date.today() and not self.pk:
                raise ValidationError("La date d'arrivée ne peut pas être dans le passé.")

    def est_disponible(self):
        """Vérifie que la chambre n'est pas déjà réservée sur ces dates."""
        qs = Reservation.objects.filter(
            chambre=self.chambre,
            statut__in=['en_attente', 'confirmee'],
            date_checkin__lt=self.date_checkout,
            date_checkout__gt=self.date_checkin,
        )
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        return not qs.exists()

    def save(self, *args, **kwargs):
        # Recalcul automatique du prix total
        if self.chambre_id and self.date_checkin and self.date_checkout:
            self.prix_total = self.calculer_prix_total()
        super().save(*args, **kwargs)
