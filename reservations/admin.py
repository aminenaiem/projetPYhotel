from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'client', 'chambre', 'date_checkin', 'date_checkout', 'prix_total')
    list_filter = ('date_checkin',)
    search_fields = ('client__nom', 'client__prenom', 'chambre__numero')
    date_hierarchy = 'date_checkin'
    ordering = ('-id',)
