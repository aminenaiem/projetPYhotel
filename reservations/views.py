"""
Vues CRUD pour la gestion des réservations (version simplifiée)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Reservation
from .forms import ReservationForm

@login_required
def liste_reservations(request):
    """Liste des réservations avec recherche simple."""
    reservations = Reservation.objects.select_related('chambre', 'client').order_by('-id')
    q = request.GET.get('q', '').strip()
    
    if q:
        reservations = reservations.filter(
            Q(client__nom__icontains=q) |
            Q(client__prenom__icontains=q) |
            Q(chambre__numero__icontains=q)
        )

    paginator = Paginator(reservations, 12)
    page = request.GET.get('page', 1)
    reservations_page = paginator.get_page(page)

    return render(request, 'reservations/liste.html', {
        'reservations': reservations_page,
        'q': q,
        'total': paginator.count,
    })

@login_required
def detail_reservation(request, pk):
    """Détail d'une réservation."""
    reservation = get_object_or_404(
        Reservation.objects.select_related('chambre', 'client'), pk=pk
    )
    return render(request, 'reservations/detail.html', {'reservation': reservation})

@login_required
def ajouter_reservation(request):
    """Créer une nouvelle réservation."""
    chambre_id = request.GET.get('chambre')
    initial = {'chambre': chambre_id} if chambre_id else {}

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            messages.success(request, f"Réservation #{reservation.pk} créée !")
            return redirect('reservations:detail', pk=reservation.pk)
    else:
        form = ReservationForm(initial=initial)

    return render(request, 'reservations/form.html', {
        'form': form,
        'titre': 'Nouvelle réservation',
        'action': 'Réserver',
    })

@login_required
def modifier_reservation(request, pk):
    """Modifier une réservation."""
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, f"Réservation #{reservation.pk} mise à jour !")
            return redirect('reservations:detail', pk=reservation.pk)
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'reservations/form.html', {
        'form': form,
        'reservation': reservation,
        'titre': 'Modifier la réservation',
        'action': 'Enregistrer',
    })

@login_required
def supprimer_reservation(request, pk):
    """Supprimer une réservation."""
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        res_id = reservation.pk
        reservation.delete()
        messages.success(request, f"Réservation #{res_id} supprimée.")
        return redirect('reservations:liste')
    return render(request, 'reservations/confirmer_suppression.html', {'reservation': reservation})
