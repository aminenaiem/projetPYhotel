from django.contrib import admin
from .models import Chambre

@admin.register(Chambre)
class ChambreAdmin(admin.ModelAdmin):
    list_display = ('numero', 'prix', 'disponible')
    list_filter = ('disponible',)
    search_fields = ('numero',)
    list_editable = ('disponible', 'prix')
    ordering = ('numero',)
