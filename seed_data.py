import os
import sys
import django
import random
from datetime import date, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from django.contrib.auth.models import User
from faker import Faker
from rooms.models import Chambre
from clients.models import Client
from reservations.models import Reservation

fake = Faker('fr_FR')
Faker.seed(42)
random.seed(42)

def reset_db():
    """Vide toutes les tables."""
    print("\n[CLEAN] Nettoyage des donnees...")
    Reservation.objects.all().delete()
    Client.objects.all().delete()
    Chambre.objects.all().delete()
    User.objects.filter(is_superuser=False).exclude(username='admin').delete()
    print("   [OK] Tables videes.\n")

def creer_superuser():
    """Cree admin / admin123."""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@hotel.ma',
            password='admin123'
        )
        print("Superuser cree -> admin / admin123")

def creer_chambres(n=20):
    """Cree n chambres simples."""
    print(f"\n[CHAMBRES] Creation de {n} chambres...")
    chambres = []
    for i in range(1, n + 1):
        chambre = Chambre.objects.create(
            numero=str(100 + i),
            prix=random.randint(400, 1200),
            disponible=True
        )
        chambres.append(chambre)
    return chambres

def creer_clients(n=30):
    """Cree n clients simples."""
    print(f"\n[CLIENTS] Creation de {n} clients...")
    clients = []
    for _ in range(n):
        client = Client.objects.create(
            nom=fake.last_name(),
            prenom=fake.first_name(),
            email=fake.unique.email(),
            telephone=fake.phone_number()[:20]
        )
        clients.append(client)
    return clients

def creer_reservations(chambres, clients, n=50):
    """Cree n reservations simples."""
    print(f"\n[RESERVATIONS] Creation de {n} reservations...")
    today = date.today()
    for _ in range(n):
        chambre = random.choice(chambres)
        client = random.choice(clients)
        
        # Dates aleatoires
        checkin = today + timedelta(days=random.randint(-30, 30))
        checkout = checkin + timedelta(days=random.randint(1, 7))
        
        Reservation.objects.create(
            chambre=chambre,
            client=client,
            date_checkin=checkin,
            date_checkout=checkout
        )
    print(f"    {n} reservations crees.")

if __name__ == '__main__':
    try:
        reset_db()
        creer_superuser()
        chambres = creer_chambres(24)
        clients = creer_clients(40)
        creer_reservations(chambres, clients, 60)
        print("\n[FIN] Base de donnee simplifiee et peuplee avec succes !\n")
    except Exception as e:
        print(f"Erreur : {e}")
        import traceback
        traceback.print_exc()
