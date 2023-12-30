from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel, Room, Booking, Review
from .forms import BookingForm, RegistrationForm, ManageBookingsForm, ReviewForm, CustomUserCreationForm
from .forms import HotelRegistrationForm, HotelUpdateForm, AddRoomForm, RoomUpdateForm, ManageAdminBookingsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
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

class RoomListView(ListView):
    model = Room
    template_name = 'main/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        hotel_id = self.kwargs['pk']
        hotel = Hotel.objects.get(pk=hotel_id)
        return Room.objects.filter(hotel=hotel, available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hotel_id = self.kwargs['pk']
        context['hotel'] = Hotel.objects.get(pk=hotel_id)
        return context


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
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'main/register_admin.html', {'form': form})


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
            return redirect('manage-rooms', pk=pk)
    else:
        form = AddRoomForm()

    return render(request, 'main/add_room.html', {'form': form, 'hotel': hotel})

@login_required
def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('manage-rooms', pk=room.hotel.pk)

    return render(request, 'main/delete_room.html', {'room': room})

@login_required
def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        form = RoomUpdateForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('info-room', pk=pk)
    else:
        form = RoomUpdateForm(instance=room)

    return render(request, 'main/edit_room.html', {'form': form, 'room': room})

@login_required
def info_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'main/info_room.html', {'room': room, 'user_hotel': room.hotel})


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


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    room = booking.room
    room.available = True  # Пометить комнату как доступную
    room.save()

    booking.delete()

    return redirect('manage-bookings')


@login_required
def manage_bookings(request, hotel_id=None, room_id=None):
    hotels = Hotel.objects.all()
    rooms = Room.objects.all()
    user_bookings = Booking.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ManageBookingsForm(request.POST, hotels=hotels, rooms=rooms)
        if form.is_valid():
            selected_hotel_id = form.cleaned_data['hotel']
            selected_room_id = form.cleaned_data['room']

            return redirect('manage-bookings', hotel_id=selected_hotel_id, room_id=selected_room_id)
    else:
        form = ManageBookingsForm(hotels=hotels, rooms=rooms)

    context = {'user_bookings': user_bookings, 'form': form}
    return render(request, 'main/manage_bookings.html', context)


@login_required
def manage_bookings_admin(request, hotel_id=None, room_id=None):
    hotels = Hotel.objects.filter(admin=request.user)
    rooms = Room.objects.filter(hotel__admin=request.user)
    bookings = Booking.objects.filter(room__in=rooms)

    if request.method == 'POST':
        form = ManageAdminBookingsForm(request.POST, hotels=hotels, rooms=rooms)
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

            return redirect('manage-bookings-admin', hotel_id=selected_hotel_id, room_id=selected_room_id)
    else:
        form = ManageAdminBookingsForm(request.POST, hotels=hotels, rooms=rooms)

    context = {'form': form, 'hotel_id': hotel_id, 'room_id': room_id, 'bookings': bookings}
    return render(request, 'main/manage_bookings_admin.html', context)


@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    booking.status = 'approved'
    booking.save()

    return redirect('manage-bookings')


@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    booking.status = 'rejected'
    booking.save()

    return redirect('manage-bookings')


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
def my_reviews(request):
    user_reviews = Review.objects.filter(user=request.user, deleted=False)

    context = {'user_reviews': user_reviews}
    return render(request, 'main/my_reviews.html', context)


def view_reviews(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    public_reviews = Review.objects.filter(hotel=hotel, deleted=False)

    context = {'public_reviews': public_reviews, 'hotel': hotel}
    return render(request, 'main/view_reviews.html', context)


@login_required
def view_reviews_admin(request):
    user = request.user
    hotels_admin = Hotel.objects.filter(admin=user)
    reviews = Review.objects.filter(hotel__in=hotels_admin)

    context = {'reviews': reviews}
    return render(request, 'main/view_reviews_admin.html', context)


@login_required
def update_reviews(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('my-reviews')
    else:
        form = ReviewForm(instance=review)

    context = {'form': form, 'review': review}
    return render(request, 'main/update_review.html', context)


@login_required
def delete_reviews(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        if review.deleted:
            review.deleted = False
        else:
            review.deleted = True

        review.save()
        return redirect('my-reviews')

    context = {'review': review}
    return render(request, 'main/delete_review.html', context)

@login_required
def update_reviews_admin(request, review_id):
    review = get_object_or_404(Review, id=review_id, hotel__admin=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('view-reviews-admin')
    else:
        form = ReviewForm(instance=review)

    context = {'form': form, 'review': review}
    return render(request, 'main/update_review_admin.html', context)


@login_required
def delete_reviews_admin(request, review_id):
    review = get_object_or_404(Review, id=review_id, hotel__admin=request.user)

    if request.method == 'POST':
        if review.deleted:
            review.deleted = False
        else:
            review.deleted = True

        review.save()
        return redirect('view-reviews-admin')

    context = {'review': review}
    return render(request, 'main/delete-reviews-admin.html', context)

