from django import forms
from .models import Event

# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = '__all__'
#         widgets = {
#             'event_date': forms.DateInput(attrs={
#                 'type': 'date',
#                 'class': 'form-control'
#             }),
#         }
# NEw
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'event_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }
        # Register
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
