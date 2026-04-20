from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'email', 'telephone',
                  'adresse', 'cin', 'nationalite', 'date_naissance']
        labels = {
            'nom': 'Nom', 'prenom': 'Prénom', 'email': 'Email',
            'telephone': 'Téléphone', 'adresse': 'Adresse',
            'cin': 'CIN / Passeport', 'nationalite': 'Nationalité',
            'date_naissance': 'Date de naissance',
        }
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 3}),
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Client.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Un client avec cet email existe déjà.")
        return email

    def clean_telephone(self):
        tel = self.cleaned_data.get('telephone', '').strip()
        if tel and not all(c in '0123456789+- ()' for c in tel):
            raise forms.ValidationError("Numéro de téléphone invalide.")
        return tel
