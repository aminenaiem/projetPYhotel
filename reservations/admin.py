from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'client', 'chambre', 'date_checkin', 'date_checkout', 'statut', 'prix_total', 'nb_nuits')
    list_filter = ('statut', 'chambre__type')
    search_fields = ('client__nom', 'client__prenom', 'chambre__numero')
    list_editable = ('statut',)
    date_hierarchy = 'date_checkin'
    ordering = ('-created_at',)
