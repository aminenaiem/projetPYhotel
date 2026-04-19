from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'email', 'telephone']
        labels = {
            'nom': 'Nom', 'prenom': 'Prénom', 'email': 'Email',
            'telephone': 'Téléphone',
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
