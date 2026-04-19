from django import forms
from .models import Chambre

class ChambreForm(forms.ModelForm):
    class Meta:
        model = Chambre
        fields = ['numero', 'prix', 'disponible']
        labels = {
            'numero': 'Numéro de chambre',
            'prix': 'Prix par nuit (MAD)',
            'disponible': 'Disponible',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

class RechercheChambresForm(forms.Form):
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
