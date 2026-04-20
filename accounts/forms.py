"""
Formulaires d'authentification et de gestion des profils
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile


class InscriptionForm(UserCreationForm):
    """Formulaire d'inscription avec champs supplémentaires."""
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=50, required=True, label="Prénom")
    last_name = forms.CharField(max_length=50, required=True, label="Nom")
    telephone = forms.CharField(max_length=20, required=False, label="Téléphone")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'telephone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style Bootstrap pour chaque champ
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            user.profile.telephone = self.cleaned_data.get('telephone', '')
            user.profile.save()
        return user


class ConnexionForm(AuthenticationForm):
    """Formulaire de connexion stylisé."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur"
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })


class ProfilForm(forms.ModelForm):
    """Mise à jour du profil utilisateur."""
    first_name = forms.CharField(max_length=50, label="Prénom")
    last_name = forms.CharField(max_length=50, label="Nom")
    email = forms.EmailField(label="Email")

    class Meta:
        model = Profile
        fields = ['telephone', 'avatar']
        labels = {'telephone': 'Téléphone', 'avatar': 'Photo de profil'}

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})
        if instance:
            initial['first_name'] = instance.user.first_name
            initial['last_name'] = instance.user.last_name
            initial['email'] = instance.user.email
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        profile.user.email = self.cleaned_data['email']
        if commit:
            profile.user.save()
            profile.save()
        return profile
