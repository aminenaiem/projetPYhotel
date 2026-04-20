"""
Tableau de bord – statistiques et recherche globale
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from rooms.models import Chambre
from clients.models import Client
from reservations.models import Reservation


@login_required
def index(request):
    """Page principale du tableau de bord."""
    today = timezone.now().date()

    # ── Statistiques principales ───────────────────────────────────────────
    stats = {
        'total_chambres': Chambre.objects.count(),
        'chambres_disponibles': Chambre.objects.filter(disponible=True).count(),
        'chambres_occupees': Chambre.objects.filter(disponible=False).count(),
        'total_clients': Client.objects.count(),
        'total_reservations': Reservation.objects.count(),
        'reservations_actives': Reservation.objects.filter(
            statut__in=['en_attente', 'confirmee']
        ).count(),
        'reservations_today': Reservation.objects.filter(date_checkin=today).count(),
        'revenu_total': Reservation.objects.filter(
            statut='confirmee'
        ).aggregate(total=Sum('prix_total'))['total'] or 0,
    }

    # ── Réservations récentes ──────────────────────────────────────────────
    reservations_recentes = (
        Reservation.objects
        .select_related('chambre', 'client')
        .order_by('-created_at')[:8]
    )

    # ── Répartition par type de chambre ───────────────────────────────────
    repartition = (
        Chambre.objects
        .values('type')
        .annotate(count=Count('id'))
        .order_by('type')
    )

    # ── Répartition par statut de réservation ─────────────────────────────
    statuts = (
        Reservation.objects
        .values('statut')
        .annotate(count=Count('id'))
    )
    statuts_dict = {s['statut']: s['count'] for s in statuts}

    # ── Chambres départs/arrivées aujourd'hui ─────────────────────────────
    arrivees_today = Reservation.objects.filter(
        date_checkin=today, statut__in=['en_attente', 'confirmee']
    ).select_related('chambre', 'client')[:5]

    departs_today = Reservation.objects.filter(
        date_checkout=today, statut='confirmee'
    ).select_related('chambre', 'client')[:5]

    return render(request, 'dashboard/index.html', {
        'stats': stats,
        'reservations_recentes': reservations_recentes,
        'repartition': repartition,
        'statuts_dict': statuts_dict,
        'arrivees_today': arrivees_today,
        'departs_today': departs_today,
        'today': today,
    })


@login_required
def recherche(request):
    """Recherche globale : chambres, réservations, clients."""
    q = request.GET.get('q', '').strip()
    resultats = {'chambres': [], 'reservations': [], 'clients': []}

    if q:
        resultats['chambres'] = Chambre.objects.filter(
            Q(numero__icontains=q) |
            Q(type__icontains=q) |
            Q(description__icontains=q)
        )[:10]

        resultats['reservations'] = Reservation.objects.filter(
            Q(client__nom__icontains=q) |
            Q(client__prenom__icontains=q) |
            Q(chambre__numero__icontains=q) |
            Q(statut__icontains=q)
        ).select_related('chambre', 'client')[:10]

        resultats['clients'] = Client.objects.filter(
            Q(nom__icontains=q) |
            Q(prenom__icontains=q) |
            Q(email__icontains=q) |
            Q(telephone__icontains=q)
        )[:10]

    total = sum(len(v) for v in resultats.values())

    return render(request, 'dashboard/recherche.html', {
        'q': q,
        'resultats': resultats,
        'total': total,
    })
