from django.forms import ModelForm, TextInput, Textarea, NumberInput
from .models import Hotel, Room, Booking, Review, User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


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

class HotelRegistrationForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'location', 'photos']

class HotelUpdateForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'location', 'photos']

class ManageRoomsForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), required=False)

class ManageBookingsForm(forms.Form):
    hotel = forms.ModelChoiceField(queryset=None)  # Заполняется в представлении
    room = forms.ModelChoiceField(queryset=None)  # Заполняется в представлении
    booking = forms.ModelChoiceField(queryset=None)  # Заполняется в представлении
    action = forms.ChoiceField(choices=[('approve', 'Одобрить'), ('reject', 'Отклонить')])


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
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите действующий адрес электронной почты.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Обязательное поле.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Обязательное поле.')
    age = forms.IntegerField(required=True, help_text='Обязательное поле.')
    passport_data = forms.CharField(max_length=20, required=True, help_text='Обязательное поле.')
    phone_number = forms.CharField(max_length=11, required=True, help_text='Обязательное поле.')

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'age', 'passport_data', 'phone_number', 'photos')


class ManageBookingsForm(forms.Form):
    hotel = forms.ChoiceField(choices=[], required=False)
    room = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        hotels = kwargs.pop('hotels', [])
        rooms = kwargs.pop('rooms', [])

        super(ManageBookingsForm, self).__init__(*args, **kwargs)

        self.fields['hotel'].choices = [(hotel.id, str(hotel)) for hotel in hotels]
        self.fields['room'].choices = [(room.id, str(room)) for room in rooms]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']

# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['user', 'room', 'check_in_date', 'check_out_date']

