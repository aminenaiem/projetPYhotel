from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ConnexionForm

def inscription(request):
    """Vue d'inscription simplifiée."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} ! Votre compte a été créé.")
            return redirect('dashboard:index')
    else:
        form = InscriptionForm()

    return render(request, 'accounts/inscription.html', {'form': form})

def connexion(request):
    """Vue de connexion simplifiée."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenue, {user.username} !")
            next_url = request.GET.get('next', 'dashboard:index')
            return redirect(next_url)
    else:
        form = ConnexionForm()

    return render(request, 'accounts/connexion.html', {'form': form})

@login_required
def deconnexion(request):
    """Déconnexion."""
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('accounts:connexion')
