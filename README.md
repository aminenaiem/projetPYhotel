# 🏨 HôtelLuxe – Système de Gestion Hôtelière Django

Application web complète de gestion d'hôtel développée avec **Django 4.2**, **MySQL** et **Bootstrap 5**.

---

## 📁 Structure du Projet

```
hotel_management/
├── hotel_management/        # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                # Authentification & profils
├── rooms/                   # Gestion des chambres
├── reservations/            # Gestion des réservations
├── clients/                 # Gestion des clients
├── dashboard/               # Tableau de bord & recherche
├── templates/               # Templates HTML (Bootstrap 5)
├── static/                  # CSS, JS, images
├── media/                   # Uploads (images chambres)
├── seed_data.py             # Données de test (Faker)
├── requirements.txt
└── .env.example
```

---

## ⚙️ Installation Complète

### 1. Prérequis

- Python 3.10+
- MySQL 8.0+
- pip

### 2. Cloner & environnement virtuel

```bash
# Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate          # Linux / macOS
venv\Scripts\activate             # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Créer la base de données MySQL

```sql
-- Dans MySQL (mysql -u root -p) :
CREATE DATABASE hotel_luxe CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hotel_user'@'localhost' IDENTIFIED BY 'motdepasse';
GRANT ALL PRIVILEGES ON hotel_luxe.* TO 'hotel_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. Configuration `.env`

```bash
# Copier le fichier exemple
cp .env.example .env

# Éditer .env avec vos valeurs
nano .env
```

Contenu de `.env` :
```
SECRET_KEY=django-insecure-changez-cette-cle-en-production
DEBUG=True
DB_NAME=hotel_luxe
DB_USER=root
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=3306
```

### 5. Migrations Django

```bash
python manage.py makemigrations accounts
python manage.py makemigrations rooms
python manage.py makemigrations clients
python manage.py makemigrations reservations
python manage.py makemigrations

python manage.py migrate
```

### 6. Générer les données de test (Faker)

```bash
# Génère 20 chambres, 50 clients, 100 réservations
python seed_data.py
```

Compte créé automatiquement :
| Champ    | Valeur     |
|----------|------------|
| Login    | `admin`    |
| Password | `admin123` |

### 7. Lancer le serveur

```bash
python manage.py runserver
```

Ouvrir : **http://127.0.0.1:8000/**

---

## 🌟 Fonctionnalités

| Module | Fonctionnalités |
|--------|----------------|
| 🔐 **Authentification** | Inscription, connexion, déconnexion, profil, rôles admin/user |
| 🏨 **Chambres** | CRUD complet, filtres, pagination, upload image |
| 📅 **Réservations** | CRUD, vérification disponibilité, calcul prix auto, changement statut |
| 👤 **Clients** | CRUD, historique réservations, recherche |
| 🔎 **Recherche** | Barre globale (navbar), résultats multi-catégories |
| 📊 **Dashboard** | Stats temps réel, arrivées/départs du jour, répartition |

---

## 🔑 Rôles Utilisateurs

| Rôle | Accès |
|------|-------|
| **Admin** | Accès complet (CRUD chambres, réservations, clients, admin Django) |
| **User** | Lecture + création de réservations |

Pour promouvoir un utilisateur en admin :
```bash
python manage.py shell
>>> from accounts.models import Profile
>>> p = Profile.objects.get(user__username='nom_utilisateur')
>>> p.role = 'admin'
>>> p.save()
```

---

## 🗄️ Modèles de Données

```
User (Django) ←──── Profile (rôle, téléphone)
                          │
Client ←──────────────────┤
   │                      │
   └── Reservation ───────┘
            │
          Chambre
```

---

## 🚀 Commandes Utiles

```bash
# Créer un superuser manuellement
python manage.py createsuperuser

# Collecter les fichiers statiques (production)
python manage.py collectstatic

# Réinitialiser et re-générer les données
python seed_data.py

# Admin Django
http://127.0.0.1:8000/admin/
```

---

## 🛠️ Technologies

- **Backend** : Django 4.2, Python 3.10+
- **BDD** : MySQL 8 + Django ORM
- **Frontend** : Bootstrap 5.3, Bootstrap Icons, Google Fonts
- **Données test** : Faker 20
- **Formulaires** : django-crispy-forms + crispy-bootstrap5
- **Config** : python-decouple (.env)
