from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel, Room, Booking
from .forms import HotelForm, BookingForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages



def home(request):
    date = {
        'title': 'Roch Hotels Official Site',
    }
    return render(request, 'main/main.html', date)

class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'main/details_view.html'
    context_object_name = 'hotels'


def room_list(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    rooms = Room.objects.filter(hotel=hotel, available=True)
    return render(request, 'main/room_list.html', {'hotel': hotel, 'rooms': rooms})


class RoomDetailView(DetailView):
    model = Room
    template_name = 'main/rooms_detail_view.html'
    context_object_name = 'room'

    def get_object(self, queryset=None):
        hotel_id = self.kwargs['pk']
        room_id = self.kwargs['room_id']
        return Room.objects.get(hotel_id=hotel_id, id=room_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class RoomListView(DetailView):
    model = Room
    template_name = 'main/room_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hotel_id = self.kwargs['pk']
        context['rooms'] = Room.objects.filter(hotel_id=hotel_id)
        context['hotel'] = Hotel.objects.get(id=hotel_id)
        return context


def about(request):
    about = {
        'about': 'Roch Hotels|Info',
    }
    return render(request, 'main/about.html', about)


def hotels(request):
    hotels = Hotel.objects.all()
    return render(request, 'main/hotels.html', {'hotels':hotels})


def create(request):
    error = ''
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotels')
        else:
            error = 'Неверное заполнение формы'

    form =HotelForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'main/create.html', data)

# @require_POST
def book_room(request, pk, room_id):
    room = get_object_or_404(Room, pk=room_id, available=True)
    booking_form = BookingForm(request.POST)

    if booking_form.is_valid():
        booking = booking_form.save(commit=False)
        booking.user = request.user
        booking.room = room
        booking.save()
        room.available = False
        room.save()
        messages.success(request, 'Комната успешно забронирована!')
        return redirect('home')
    else:
        return render(request, 'main/rooms_detail_view.html', {'room': room, 'booking_form': booking_form})

def manage_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('manage-bookings')
    else:
        form = BookingForm()

    return render(request, 'main/manage_bookings.html', {'form': form, 'bookings': bookings})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'main/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'main/profile.html')


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'main/login.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

class CustomLoginView(LoginView):
    template_name = 'main/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'path/to/logout.html'

