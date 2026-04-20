"""
Formulaires pour la gestion des chambres
"""
from django import forms
from .models import Chambre


class ChambreForm(forms.ModelForm):
    class Meta:
        model = Chambre
        fields = ['numero', 'type', 'prix', 'disponible', 'description',
                  'capacite', 'etage', 'superficie', 'image']
        labels = {
            'numero': 'Numéro de chambre',
            'type': 'Type de chambre',
            'prix': 'Prix par nuit (MAD)',
            'disponible': 'Disponible',
            'description': 'Description',
            'capacite': 'Capacité (personnes)',
            'etage': 'Étage',
            'superficie': 'Superficie (m²)',
            'image': 'Photo de la chambre',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_numero(self):
        numero = self.cleaned_data.get('numero', '').strip().upper()
        qs = Chambre.objects.filter(numero=numero)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ce numéro de chambre est déjà utilisé.")
        return numero

    def clean_prix(self):
        prix = self.cleaned_data.get('prix')
        if prix and prix <= 0:
            raise forms.ValidationError("Le prix doit être supérieur à 0.")
        return prix


class RechercheChambresForm(forms.Form):
    """Formulaire de filtrage des chambres."""
    type = forms.ChoiceField(
        choices=[('', 'Tous les types')] + Chambre.TYPE_CHOICES,
        required=False,
        label="Type",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    prix_min = forms.DecimalField(
        required=False, label="Prix min",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix min'})
    )
    prix_max = forms.DecimalField(
        required=False, label="Prix max",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix max'})
    )
    disponible = forms.ChoiceField(
        choices=[('', 'Toutes'), ('1', 'Disponibles'), ('0', 'Occupées')],
        required=False,
        label="Disponibilité",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
