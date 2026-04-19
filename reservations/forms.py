from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Reservation
from rooms.models import Chambre
from clients.models import Client

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['chambre', 'client', 'date_checkin', 'date_checkout']
        labels = {
            'chambre': 'Chambre',
            'client': 'Client',
            'date_checkin': "Date d'arrivée",
            'date_checkout': 'Date de départ',
        }
        widgets = {
            'date_checkin': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'date_checkout': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chambre'].queryset = Chambre.objects.all()
        self.fields['client'].queryset = Client.objects.all().order_by('nom', 'prenom')

        for name, field in self.fields.items():
            if name not in ('date_checkin', 'date_checkout'):
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs.update({'class': 'form-select'})
                else:
                    field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned = super().clean()
        checkin = cleaned.get('date_checkin')
        checkout = cleaned.get('date_checkout')
        chambre = cleaned.get('chambre')

        if checkin and checkout:
            if checkin >= checkout:
                raise ValidationError("La date de départ doit être postérieure à la date d'arrivée.")
            if checkin < date.today() and not self.instance.pk:
                raise ValidationError("La date d'arrivée ne peut pas être dans le passé.")

        if chambre and checkin and checkout:
            qs = Reservation.objects.filter(
                chambre=chambre,
                date_checkin__lt=checkout,
                date_checkout__gt=checkin,
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(
                    f"La chambre {chambre.numero} est déjà réservée pour ces dates."
                )

        return cleaned
