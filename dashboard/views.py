from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from rooms.models import Chambre
from clients.models import Client
from reservations.models import Reservation

@login_required
def index(request):
    """Page principale du tableau de bord simplifiée."""
    today = timezone.now().date()

    stats = {
        'total_chambres': Chambre.objects.count(),
        'chambres_disponibles': Chambre.objects.filter(disponible=True).count(),
        'total_clients': Client.objects.count(),
        'total_reservations': Reservation.objects.count(),
        'revenu_total': Reservation.objects.aggregate(total=Sum('prix_total'))['total'] or 0,
    }

    reservations_recentes = (
        Reservation.objects
        .select_related('chambre', 'client')
        .order_by('-id')[:8]
    )

    arrivees_today = Reservation.objects.filter(
        date_checkin=today
    ).select_related('chambre', 'client')[:5]

    departs_today = Reservation.objects.filter(
        date_checkout=today
    ).select_related('chambre', 'client')[:5]

    return render(request, 'dashboard/index.html', {
        'stats': stats,
        'reservations_recentes': reservations_recentes,
        'arrivees_today': arrivees_today,
        'departs_today': departs_today,
        'today': today,
    })

@login_required
def recherche(request):
    """Recherche globale simplifiée."""
    q = request.GET.get('q', '').strip()
    resultats = {'chambres': [], 'reservations': [], 'clients': []}

    if q:
        resultats['chambres'] = Chambre.objects.filter(
            Q(numero__icontains=q)
        )[:10]

        resultats['reservations'] = Reservation.objects.filter(
            Q(client__nom__icontains=q) |
            Q(client__prenom__icontains=q) |
            Q(chambre__numero__icontains=q)
        ).select_related('chambre', 'client')[:10]

        resultats['clients'] = Client.objects.filter(
            Q(nom__icontains=q) |
            Q(prenom__icontains=q) |
            Q(email__icontains=q)
        )[:10]

    total = sum(len(v) for v in resultats.values())

    return render(request, 'dashboard/recherche.html', {
        'q': q,
        'resultats': resultats,
        'total': total,
    })
