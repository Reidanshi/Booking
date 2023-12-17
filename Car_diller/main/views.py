from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel, Room, Booking, Review
from .forms import HotelForm, BookingForm, RegistrationForm, ManageBookingsForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView



def home(request):
    date = {
        'title': 'Roch Hotels Official Site',
    }
    return render(request, 'main/main.html', date)

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    reviews = Review.objects.filter(hotel=hotel)
    context = {'hotel': hotel, 'reviews': reviews}
    return render(request, 'main/hotel_detail.html', context)

# class HotelDetailView(DetailView):
#     model = Hotel
#     template_name = 'main/details_view.html'
#     context_object_name = 'hotels'

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
    room = get_object_or_404(Room, pk=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()

            room.is_booked = True
            room.save()

            return redirect('manage-bookings')

    else:
        form = BookingForm()

    context = {
        'room': room,
        'form': form,
    }

    return render(request, 'main/book_room.html', context)

def book_room(request, pk, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()

            room.is_booked = True
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


@login_required
def view_reviews(request, pk):
    user_reviews = Review.objects.filter(user=request.user)
    return render(request, 'main/view_reviews.html', {'user_reviews': user_reviews})

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




