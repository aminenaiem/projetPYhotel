from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'telephone', 'nationalite', 'nb_reservations', 'created_at')
    search_fields = ('nom', 'prenom', 'email', 'cin')
    list_filter = ('nationalite',)
    ordering = ('nom', 'prenom')
