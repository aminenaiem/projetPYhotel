from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'telephone')
    search_fields = ('nom', 'prenom', 'email')
    ordering = ('nom', 'prenom')
