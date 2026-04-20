from django.contrib import admin
from .models import Chambre


@admin.register(Chambre)
class ChambreAdmin(admin.ModelAdmin):
    list_display = ('numero', 'type', 'prix', 'disponible', 'capacite', 'etage')
    list_filter = ('type', 'disponible', 'etage')
    search_fields = ('numero', 'description')
    list_editable = ('disponible', 'prix')
    ordering = ('numero',)
