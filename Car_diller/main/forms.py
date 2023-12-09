from django.forms import ModelForm, TextInput, Textarea, NumberInput
from .models import Hotel

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
