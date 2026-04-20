"""
Vues pour l'authentification et la gestion des profils
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ConnexionForm, ProfilForm


def inscription(request):
    """Vue d'inscription d'un nouvel utilisateur."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.first_name} ! Votre compte a été créé.")
            return redirect('dashboard:index')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = InscriptionForm()

    return render(request, 'accounts/inscription.html', {'form': form})


def connexion(request):
    """Vue de connexion."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenue, {user.first_name or user.username} !")
            next_url = request.GET.get('next', 'dashboard:index')
            return redirect(next_url)
        else:
            messages.error(request, "Identifiants incorrects. Veuillez réessayer.")
    else:
        form = ConnexionForm()

    return render(request, 'accounts/connexion.html', {'form': form})


@login_required
def deconnexion(request):
    """Déconnexion de l'utilisateur."""
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('accounts:connexion')


@login_required
def profil(request):
    """Vue et modification du profil utilisateur."""
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès !")
            return redirect('accounts:profil')
        else:
            messages.error(request, "Erreur lors de la mise à jour du profil.")
    else:
        form = ProfilForm(instance=profile)

    return render(request, 'accounts/profil.html', {'form': form, 'profile': profile})
