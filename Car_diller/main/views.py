from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel, Room, Booking, Review
from .forms import BookingForm, RegistrationForm, ManageBookingsForm, ReviewForm, CustomUserCreationForm
from .forms import HotelRegistrationForm, HotelUpdateForm, AddRoomForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from datetime import date
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


def home(request):
    context = {
        'title': 'Roch Hotels Official Site',
        'user': request.user
    }
    return render(request, 'main/main.html', context)


def hotels(request):
    hotels = Hotel.objects.all()
    return render(request, 'main/hotels.html', {'hotels':hotels})


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    reviews = Review.objects.filter(hotel=hotel)
    context = {'hotel': hotel, 'reviews': reviews}
    return render(request, 'main/hotel_detail.html', context)

@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')


class CustomLoginView(LoginView):
    template_name = 'main/login.html'



def register_admin(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # Делаем пользователя администратором
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'main/register_admin.html', {'form': form})


@login_required
def hotel_reviews(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    reviews = Review.objects.filter(hotel=hotel)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.hotel = hotel
            review.user = request.user
            review.save()
            return redirect('hotel-reviews', pk=pk)

    context = {
        'hotel': hotel,
        'reviews': reviews,
        'form': form,
    }

    return render(request, 'main/hotel_reviews.html', context)

@login_required
def update_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('hotel-reviews', pk=review.hotel.pk)
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review': review,
    }

    return render(request, 'main/update_review.html', context)

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    hotel_pk = review.hotel.pk
    review.delete()
    return redirect('hotel-reviews', pk=hotel_pk)


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



@login_required
def book_room(request, pk, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()

            room.available = False
            room.save()

            return redirect('manage-bookings')

    else:
        form = BookingForm()

    context = {
        'room': room,
        'form': form,
    }

    return render(request, 'main/book_room.html', context)


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    room = booking.room
    room.is_booked = False
    room.save()

    booking.delete()

    return redirect('manage-bookings')


def manage_bookings(request, hotel_id=None, room_id=None):
    hotels = Hotel.objects.all()
    rooms = Room.objects.all()
    bookings = Booking.objects.all()

    if request.method == 'POST':
        form = ManageBookingsForm(request.POST, hotels=hotels, rooms=rooms)
        if form.is_valid():
            selected_hotel_id = form.cleaned_data['hotel']
            selected_room_id = form.cleaned_data['room']

            return redirect('manage-bookings', hotel_id=selected_hotel_id, room_id=selected_room_id)
    else:
        form = ManageBookingsForm(hotels=hotels, rooms=rooms)

    context = {'form': form, 'hotel_id': hotel_id, 'room_id': room_id}
    return render(request, 'main/manage_bookings.html', {'bookings': bookings})


@login_required
def register_hotel(request):
    if request.method == 'POST':
        form = HotelRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.admin = request.user
            hotel.save()
            messages.success(request, 'Отель успешно зарегистрирован!')
            return redirect('my-hotel')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = HotelRegistrationForm()

    return render(request, 'main/register_hotel.html', {'form': form})


@login_required
def my_hotel(request):
    user_hotel = Hotel.objects.filter(admin=request.user).first()
    return render(request, 'main/my_hotel.html', {'user_hotel': user_hotel})

@login_required
def view_reviews_admin(request):
    return render(request, 'main/view_reviews_admin.html')

@login_required
def update_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    if hotel.admin != request.user:
        return HttpResponseForbidden("Вы не являетесь администратором этого отеля.")

    if request.method == 'POST':
        form = HotelUpdateForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('my-hotel', pk=hotel.pk)
    else:
        form = HotelUpdateForm(instance=hotel)

    return render(request, 'main/update_hotel.html', {'form': form, 'hotel': hotel})

@login_required
def delete_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    if hotel.admin != request.user:
        return HttpResponseForbidden("Вы не являетесь администратором этого отеля.")

    if request.method == 'POST':
        hotel.delete()
        return redirect('home')

    return render(request, 'main/delete_hotel.html', {'hotel': hotel})


@login_required
def manage_rooms(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    if hotel.admin != request.user:
        return HttpResponseForbidden("Вы не являетесь администратором этого отеля.")

    rooms = Room.objects.filter(hotel=hotel)

    return render(request, 'main/manage_rooms.html', {'hotel': hotel, 'rooms': rooms})


@login_required
def add_room(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    if request.method == 'POST':
        form = AddRoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            hotel.room.add(room)
            messages.success(request, 'Комната успешно зарегистрирована!')
            return redirect('manage-rooms', pk=pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = AddRoomForm()

    return render(request, 'main/add_room.html', {'form': form, 'hotel': hotel})



@login_required
def manage_bookings(request, hotel_id=None, room_id=None):
    hotels = Hotel.objects.get_for_admin(request.user)
    if not hotels.exists():
        return HttpResponseForbidden("У вас нет прав для управления бронированиями отелей.")

    rooms = Room.objects.filter(hotel__admin=request.user)
    bookings = Booking.objects.filter(room__in=rooms)

    if request.method == 'POST':
        form = ManageBookingsForm(request.POST, hotels=hotels, rooms=rooms)
        if form.is_valid():
            selected_hotel_id = form.cleaned_data['hotel']
            selected_room_id = form.cleaned_data['room']
            selected_booking_id = form.cleaned_data['booking']

            if form.cleaned_data['action'] == 'approve':
                booking = Booking.objects.get(id=selected_booking_id)
                booking.status = 'approved'
                booking.save()
            elif form.cleaned_data['action'] == 'reject':
                booking = Booking.objects.get(id=selected_booking_id)
                booking.status = 'rejected'
                booking.save()

            return redirect('manage-bookings', hotel_id=selected_hotel_id, room_id=selected_room_id)
    else:
        form = ManageBookingsForm(hotels=hotels, rooms=rooms)

    context = {'form': form, 'hotel_id': hotel_id, 'room_id': room_id}
    return render(request, 'main/manage_bookings.html', {'bookings': bookings, 'form': form})

@user_passes_test(lambda u: u.is_staff)
def manage_bookings_admin(request, hotel_id=None, room_id=None):
    bookings = Booking.objects.all()

    context = {'bookings': bookings}
    return render(request, 'main/manage_bookings_admin.html', context)

@login_required
def add_review(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.hotel = hotel
            review.save()
            return redirect('hotel-detail', pk=hotel_id)
    else:
        form = ReviewForm()

    return render(request, 'main/add_review.html', {'form': form, 'hotel': hotel})



def view_reviews(request, pk):
    user_reviews = Review.objects.filter(user=request.user)
    return render(request, 'main/view_reviews.html', {'user_reviews': user_reviews})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
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




class HotelCreateView(CreateView):
    model = Hotel
    template_name = 'hotel_form.html'
    fields = ['name', 'description', 'location', 'photos']


class HotelUpdateView(UpdateView):
    model = Hotel
    template_name = 'hotel_form.html'
    fields = ['name', 'description', 'location', 'photos']


class HotelDeleteView(DeleteView):
    model = Hotel
    template_name = 'hotel_confirm_delete.html'
    success_url = reverse_lazy('hotel-list')

class HotelReviewsView(ListView):
    model = Review
    template_name = 'hotel_reviews.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Review.objects.filter(hotel_id=self.kwargs['pk'])

class RoomCreateView(CreateView):
    model = Room
    template_name = 'room_form.html'
    fields = ['room_type', 'description', 'beds_counter', 'number_room', 'level', 'photos', 'price_per_night', 'available']


class RoomUpdateView(UpdateView):
    model = Room
    template_name = 'room_form.html'
    fields = ['room_type', 'description', 'beds_counter', 'number_room', 'level', 'photos', 'price_per_night', 'available']


class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'room_confirm_delete.html'
    success_url = reverse_lazy('hotel-list')

class RoomAvailabilityView(UpdateView):
    model = Room
    template_name = 'room_availability.html'
    fields = ['available']
    success_url = reverse_lazy('hotel-list')

class ReservationListView(ListView):
    model = Booking
    template_name = 'reservation_list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        today = date.today()
        return Booking.objects.filter(Q(check_out_date__gte=today) | Q(check_in_date__gte=today))

def booking_list(request):
    bookings = Booking.objects.all()  # предполагается, что у вас есть модель Booking
    return render(request, 'main/booking_list.html', {'bookings': bookings})

def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'main/booking_list.html', {'bookings': bookings})

def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()
    return redirect('booking-list')

def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking-list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'main/edit_booking.html', {'form': form, 'booking': booking})