from .models import Hotel
from django.forms import ModelForm, TextInput, Textarea


class HotelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'description']

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
            })
        }