"""
Vues CRUD pour la gestion des clients
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Client
from .forms import ClientForm


@login_required
def liste_clients(request):
    """Liste des clients avec recherche et pagination."""
    q = request.GET.get('q', '').strip()
    clients = Client.objects.all()

    if q:
        clients = clients.filter(
            Q(nom__icontains=q) | Q(prenom__icontains=q) |
            Q(email__icontains=q) | Q(telephone__icontains=q)
        )

    paginator = Paginator(clients, 10)
    page = request.GET.get('page', 1)
    clients_page = paginator.get_page(page)

    return render(request, 'clients/liste.html', {
        'clients': clients_page,
        'q': q,
        'total': paginator.count,
    })


@login_required
def detail_client(request, pk):
    """Profil détaillé d'un client avec son historique de réservations."""
    client = get_object_or_404(Client, pk=pk)
    reservations = client.reservation_set.select_related('chambre').order_by('-date_checkin')
    return render(request, 'clients/detail.html', {
        'client': client,
        'reservations': reservations,
    })


@login_required
def ajouter_client(request):
    """Créer un nouveau client."""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f"Client {client.nom_complet} ajouté avec succès !")
            return redirect('clients:detail', pk=client.pk)
        else:
            messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = ClientForm()

    return render(request, 'clients/form.html', {
        'form': form,
        'titre': 'Ajouter un client',
        'action': 'Ajouter',
    })


@login_required
def modifier_client(request, pk):
    """Modifier les informations d'un client."""
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Informations client mises à jour !")
            return redirect('clients:detail', pk=client.pk)
        else:
            messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/form.html', {
        'form': form,
        'client': client,
        'titre': f'Modifier – {client.nom_complet}',
        'action': 'Enregistrer',
    })


@login_required
def supprimer_client(request, pk):
    """Supprimer un client (avec confirmation)."""
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        nom = client.nom_complet
        client.delete()
        messages.success(request, f"Client {nom} supprimé.")
        return redirect('clients:liste')

    return render(request, 'clients/confirmer_suppression.html', {'client': client})
