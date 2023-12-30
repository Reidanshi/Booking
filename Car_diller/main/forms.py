from django.forms import ModelForm, TextInput, Textarea, NumberInput
from .models import Hotel, Room, Booking, Review, User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class HotelRegistrationForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'description', 'photos', 'room_count', 'phone_number', 'email', 'address']

class HotelUpdateForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'description', 'photos', 'room_count', 'phone_number', 'email', 'address']



class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'description', 'beds_counter', 'number_room', 'level', 'photos', 'price_per_night']

class RoomUpdateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'description', 'beds_counter', 'number_room', 'level', 'photos', 'price_per_night']

class ManageAdminBookingsForm(forms.Form):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all())
    room = forms.ModelChoiceField(queryset=Room.objects.all())
    booking = forms.ModelChoiceField(queryset=Booking.objects.all())
    action = forms.ChoiceField(choices=[('approve', 'Одобрить'), ('reject', 'Отклонить')])

    def __init__(self, *args, hotels=None, rooms=None, **kwargs):
        super(ManageAdminBookingsForm, self).__init__(*args, **kwargs)
        if hotels is not None:
            self.fields['hotel'].queryset = hotels
        if rooms is not None:
            self.fields['room'].queryset = rooms


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'status']

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



