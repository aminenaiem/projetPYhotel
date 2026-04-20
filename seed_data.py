"""
╔══════════════════════════════════════════════════════════════╗
║         SCRIPT DE GÉNÉRATION DE DONNÉES DE TEST              ║
║   Génère : 20 chambres, 50 clients, 100 réservations         ║
║   Utilisation : python seed_data.py                          ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import django
import random
from datetime import date, timedelta

# ── Configuration Django ──────────────────────────────────────────────────────
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from django.contrib.auth.models import User
from faker import Faker
from rooms.models import Chambre
from clients.models import Client
from reservations.models import Reservation
from accounts.models import Profile

fake = Faker('fr_FR')
Faker.seed(42)
random.seed(42)

# ─────────────────────────────────────────────────────────────────────────────
def reset_db():
    """Vide les tables avant de régénérer."""
    print("🗑️  Nettoyage des données existantes...")
    Reservation.objects.all().delete()
    Client.objects.all().delete()
    Chambre.objects.all().delete()
    User.objects.filter(is_superuser=False).exclude(username='admin').delete()
    print("   ✓ Tables vidées.\n")


# ─────────────────────────────────────────────────────────────────────────────
def creer_superuser():
    """Crée un compte administrateur si inexistant."""
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@hotelluxe.ma',
            password='admin123',
            first_name='Admin',
            last_name='HôtelLuxe',
        )
        admin.profile.role = 'admin'
        admin.profile.save()
        print("👑  Superuser créé → admin / admin123")
    else:
        print("👑  Superuser 'admin' déjà existant.")


# ─────────────────────────────────────────────────────────────────────────────
def creer_utilisateurs(n=5):
    """Crée des utilisateurs staff."""
    print(f"\n👤  Création de {n} utilisateurs...")
    users = [User.objects.get(username='admin')]

    for i in range(n):
        prenom = fake.first_name()
        nom = fake.last_name()
        username = f"{prenom.lower()}.{nom.lower()}{i}"[:30]
        if User.objects.filter(username=username).exists():
            username = f"{username}_{i}"

        user = User.objects.create_user(
            username=username,
            email=fake.email(),
            password='password123',
            first_name=prenom,
            last_name=nom,
        )
        user.profile.telephone = fake.phone_number()[:20]
        user.profile.save()
        users.append(user)

    print(f"   ✓ {n} utilisateurs créés.")
    return users


# ─────────────────────────────────────────────────────────────────────────────
def creer_chambres(n=20):
    """Génère 20 chambres réalistes."""
    print(f"\n🏨  Création de {n} chambres...")

    types = ['simple', 'double', 'suite', 'deluxe', 'familiale']
    descriptions = {
        'simple': [
            "Chambre confortable avec vue sur le jardin, dotée d'une literie de qualité et d'une salle de bain privée.",
            "Chambre cosy idéale pour un voyage d'affaires, avec bureau ergonomique et connexion Wi-Fi haut débit.",
        ],
        'double': [
            "Grande chambre double avec lit king-size, décoration raffinée et vue panoramique sur la ville.",
            "Chambre double élégante avec balcon privé, parfaite pour les couples en escapade romantique.",
        ],
        'suite': [
            "Suite luxueuse composée d'un salon séparé, d'une chambre royale et d'une salle de bain en marbre.",
            "Suite présidentielle avec jacuzzi, terrasse panoramique et service de conciergerie dédié.",
        ],
        'deluxe': [
            "Chambre deluxe spacieuse avec parquet en bois, plafonds hauts et vue imprenable sur la piscine.",
            "Expérience deluxe incomparable avec mini-bar premium, lit superking et literie 5 étoiles.",
        ],
        'familiale': [
            "Suite familiale avec deux chambres communicantes, espace jeux pour enfants et kitchenette équipée.",
            "Chambre familiale généreuse pouvant accueillir jusqu'à 4 personnes avec lits superposés et coin salon.",
        ],
    }
    prix_base = {
        'simple': (300, 600),
        'double': (500, 900),
        'suite': (1200, 2500),
        'deluxe': (800, 1500),
        'familiale': (700, 1200),
    }
    capacite_map = {'simple': 1, 'double': 2, 'suite': 2, 'deluxe': 2, 'familiale': 4}

    chambres = []
    numeros_utilises = set()
    etages = [1, 2, 3, 4, 5]

    for i in range(n):
        type_ch = types[i % len(types)]
        etage = etages[i % len(etages)]

        # Numéro unique type 101, 202, 303...
        numero_base = etage * 100 + (i % 20) + 1
        numero = str(numero_base)
        while numero in numeros_utilises:
            numero_base += 1
            numero = str(numero_base)
        numeros_utilises.add(numero)

        min_prix, max_prix = prix_base[type_ch]
        prix = round(random.uniform(min_prix, max_prix), 2)
        superficie = {'simple': 20, 'double': 30, 'suite': 60, 'deluxe': 45, 'familiale': 55}[type_ch]

        chambre = Chambre.objects.create(
            numero=numero,
            type=type_ch,
            prix=prix,
            disponible=random.choice([True, True, True, False]),  # 75% dispo
            description=random.choice(descriptions[type_ch]),
            capacite=capacite_map[type_ch],
            etage=etage,
            superficie=superficie + random.randint(-5, 15),
        )
        chambres.append(chambre)

    print(f"   ✓ {n} chambres créées.")
    return chambres


# ─────────────────────────────────────────────────────────────────────────────
def creer_clients(n=50):
    """Génère 50 clients avec données réalistes."""
    print(f"\n👥  Création de {n} clients...")

    nationalites = [
        'Marocaine', 'Française', 'Espagnole', 'Allemande', 'Britannique',
        'Italienne', 'Américaine', 'Canadienne', 'Belge', 'Suisse',
        'Tunisienne', 'Algérienne', 'Sénégalaise', 'Qatarie', 'Émiratie',
    ]

    clients = []
    emails_utilises = set()

    for _ in range(n):
        prenom = fake.first_name()
        nom = fake.last_name()
        email_base = f"{prenom.lower()}.{nom.lower()}@{fake.free_email_domain()}"
        email = email_base
        counter = 1
        while email in emails_utilises:
            email = f"{prenom.lower()}.{nom.lower()}{counter}@{fake.free_email_domain()}"
            counter += 1
        emails_utilises.add(email)

        client = Client.objects.create(
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=fake.phone_number()[:20],
            adresse=fake.address()[:200],
            cin=fake.bothify(text='??######').upper(),
            nationalite=random.choice(nationalites),
            date_naissance=fake.date_of_birth(minimum_age=18, maximum_age=80),
        )
        clients.append(client)

    print(f"   ✓ {n} clients créés.")
    return clients


# ─────────────────────────────────────────────────────────────────────────────
def creer_reservations(chambres, clients, users, n=100):
    """Génère 100 réservations en respectant les contraintes métier."""
    print(f"\n📅  Création de {n} réservations...")

    statuts = ['en_attente', 'confirmee', 'confirmee', 'terminee', 'annulee']
    count = 0
    tentatives = 0
    max_tentatives = n * 5

    # Dates : répartition sur les 6 prochains mois + 3 mois passés
    today = date.today()
    date_debut_range = today - timedelta(days=90)
    date_fin_range   = today + timedelta(days=180)

    while count < n and tentatives < max_tentatives:
        tentatives += 1
        chambre = random.choice(chambres)
        client  = random.choice(clients)
        user    = random.choice(users)

        # Générer des dates aléatoires
        nb_jours_debut = random.randint(0, (date_fin_range - date_debut_range).days)
        checkin  = date_debut_range + timedelta(days=nb_jours_debut)
        nb_nuits = random.randint(1, 14)
        checkout = checkin + timedelta(days=nb_nuits)

        # Vérifier la disponibilité
        conflit = Reservation.objects.filter(
            chambre=chambre,
            statut__in=['en_attente', 'confirmee'],
            date_checkin__lt=checkout,
            date_checkout__gt=checkin,
        ).exists()

        if conflit:
            continue

        statut = random.choice(statuts)
        # Les réservations passées sont terminées ou annulées
        if checkout < today and statut in ['en_attente', 'confirmee']:
            statut = random.choice(['terminee', 'annulee'])
        # Les réservations futures ne sont pas "terminées"
        if checkin > today and statut == 'terminee':
            statut = 'confirmee'

        Reservation.objects.create(
            chambre=chambre,
            client=client,
            user=user,
            date_checkin=checkin,
            date_checkout=checkout,
            statut=statut,
            nb_personnes=random.randint(1, chambre.capacite),
            notes=fake.text(max_nb_chars=120) if random.random() > 0.6 else '',
        )
        count += 1

    print(f"   ✓ {count} réservations créées ({tentatives} tentatives).")
    return count


# ─────────────────────────────────────────────────────────────────────────────
def afficher_resume():
    print("\n" + "═" * 55)
    print("  📊  RÉSUMÉ DE LA BASE DE DONNÉES")
    print("═" * 55)
    print(f"  👤  Utilisateurs   : {User.objects.count()}")
    print(f"  🏨  Chambres       : {Chambre.objects.count()}")
    print(f"  👥  Clients        : {Client.objects.count()}")
    print(f"  📅  Réservations   : {Reservation.objects.count()}")
    print("═" * 55)
    print("\n  🔑  Compte admin :")
    print("      URL      : http://127.0.0.1:8000/")
    print("      Login    : admin")
    print("      Password : admin123")
    print("═" * 55 + "\n")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n🚀  Démarrage du script de génération de données...\n")

    try:
        reset_db()
        creer_superuser()
        users    = creer_utilisateurs(5)
        chambres = creer_chambres(20)
        clients  = creer_clients(50)
        creer_reservations(chambres, clients, users, 100)
        afficher_resume()
        print("✅  Terminé avec succès !\n")

    except Exception as e:
        print(f"\n❌  Erreur : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
