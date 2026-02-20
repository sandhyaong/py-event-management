from django import forms  # <--- This line is missing!
from .models import Event
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'event_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email'] # UserCreationForm handles passwords internally


# Booking
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_tickets']