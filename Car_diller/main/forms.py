from django.forms import ModelForm, TextInput, Textarea, NumberInput
from .models import Hotel, Room, Booking
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class HotelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'description', 'rating']

        widgets = {
            "name": TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Название отеля'
            }),
            "location": TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Локация'
            }),
            "description": Textarea(attrs={
                'class': "form-control",
                'placeholder': 'Описание отеля'
            }),
            "rating": NumberInput(attrs={
                'class': "form-control",
                'placeholder': 'Рейтинг'
            })
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date']

        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']