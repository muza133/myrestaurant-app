from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'date', 'time', 'guests_count', 'reason', 'special_request']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Emailingiz', 'required': True}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'required': True}),
            'guests_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Odamlar soni', 'min': 1, 'required': True}),
            'reason': forms.Select(attrs={'class': 'form-select'}),
            'special_request': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Qo\'shimcha istaklar', 'style': 'height: 100px'}),
        }