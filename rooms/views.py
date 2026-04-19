"""
Vues CRUD pour la gestion des chambres (version simplifiée)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Chambre
from .forms import ChambreForm, RechercheChambresForm

def admin_required(view_func):
    """Décorateur : réserve la vue aux administrateurs (Staff)."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "Accès réservé aux administrateurs.")
            return redirect('dashboard:index')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def liste_chambres(request):
    """Liste des chambres avec filtres simples."""
    chambres = Chambre.objects.all()
    form = RechercheChambresForm(request.GET)

    if form.is_valid():
        if form.cleaned_data.get('prix_min'):
            chambres = chambres.filter(prix__gte=form.cleaned_data['prix_min'])
        if form.cleaned_data.get('prix_max'):
            chambres = chambres.filter(prix__lte=form.cleaned_data['prix_max'])
        if form.cleaned_data.get('disponible') != '':
            dispo = form.cleaned_data['disponible'] == '1'
            chambres = chambres.filter(disponible=dispo)

    # Tri simple
    tri = request.GET.get('tri', 'numero')
    if tri in ['numero', 'prix', '-prix']:
        chambres = chambres.order_by(tri)

    paginator = Paginator(chambres, 12)
    page = request.GET.get('page', 1)
    chambres_page = paginator.get_page(page)

    return render(request, 'rooms/liste.html', {
        'chambres': chambres_page,
        'form': form,
        'total': paginator.count,
    })

@login_required
def detail_chambre(request, pk):
    """Détail d'une chambre."""
    chambre = get_object_or_404(Chambre, pk=pk)
    reservations = chambre.reservation_set.order_by('-date_checkin')[:5]
    return render(request, 'rooms/detail.html', {
        'chambre': chambre,
        'reservations': reservations,
    })

@admin_required
def ajouter_chambre(request):
    """Ajouter une chambre."""
    if request.method == 'POST':
        form = ChambreForm(request.POST)
        if form.is_valid():
            chambre = form.save()
            messages.success(request, f"Chambre {chambre.numero} ajoutée !")
            return redirect('rooms:liste')
    else:
        form = ChambreForm()

    return render(request, 'rooms/form.html', {
        'form': form,
        'titre': 'Ajouter une chambre',
        'action': 'Ajouter',
    })

@admin_required
def modifier_chambre(request, pk):
    """Modifier une chambre."""
    chambre = get_object_or_404(Chambre, pk=pk)
    if request.method == 'POST':
        form = ChambreForm(request.POST, instance=chambre)
        if form.is_valid():
            form.save()
            messages.success(request, f"Chambre {chambre.numero} modifiée !")
            return redirect('rooms:detail', pk=chambre.pk)
    else:
        form = ChambreForm(instance=chambre)

    return render(request, 'rooms/form.html', {
        'form': form,
        'chambre': chambre,
        'titre': 'Modifier la chambre',
        'action': 'Enregistrer',
    })

@admin_required
def supprimer_chambre(request, pk):
    """Supprimer une chambre."""
    chambre = get_object_or_404(Chambre, pk=pk)
    if request.method == 'POST':
        numero = chambre.numero
        chambre.delete()
        messages.success(request, f"Chambre {numero} supprimée.")
        return redirect('rooms:liste')
    return render(request, 'rooms/confirmer_suppression.html', {'chambre': chambre})
