from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import register, register_admin, profile, manage_bookings, cancel_booking, view_reviews
from .views import CustomLoginView, custom_logout, hotel_detail, add_review, HotelCreateView, HotelUpdateView, update_hotel, add_room
from .views import HotelReviewsView, RoomCreateView, RoomUpdateView, RoomDeleteView, ReservationListView, delete_hotel, manage_rooms
from .views import HotelDeleteView, RoomAvailabilityView, manage_bookings_admin, view_reviews_admin, my_hotel, register_hotel

urlpatterns = [
    path('', views.home, name='home'),
    path('hotels/', views.hotels, name='hotels'),
    path('hotels/<int:pk>/', hotel_detail, name='hotel-detail'),
    path('hotels/<int:pk>/rooms/', views.RoomListView.as_view(), name='room-list'),
    path('hotels/<int:pk>/rooms/<int:room_id>', views.RoomDetailView.as_view(), name='room-detail'),
    path('register/', register, name='register'),
    path('register/admin/', register_admin, name='register_admin'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', custom_logout, name='logout'),
    path('register-hotel/', register_hotel, name='register-hotel'),
    path('my-hotel/', my_hotel, name='my-hotel'),
    path('edit-hotel/<int:pk>/', update_hotel, name='edit-hotel'),
    path('manage-rooms/<int:pk>/', manage_rooms, name='manage-rooms'),
    path('add-room/<int:pk>/', add_room, name='add-room'),
    path('delete-hotel/<int:pk>/', delete_hotel, name='delete-hotel'),
    path('manage-bookings-admin/', manage_bookings_admin, name='manage-bookings-admin'),
    path('view-reviews-admin/', view_reviews_admin, name='view-reviews-admin'),
    path('hotels/<int:pk>/rooms/<int:room_id>/book/', views.book_room, name='book-room'),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel-booking'),
    path('manage-bookings/', manage_bookings, name='manage-bookings'),
    path('manage-bookings/admin/', manage_bookings_admin, name='manage-bookings-admin'),
    path('hotels/<int:hotel_id>/add-review/', add_review, name='add-review'),
    path('my-reviews/<int:pk>/', view_reviews, name='view-reviews'),
    path('manage-bookings/<int:hotel_id>/', manage_bookings, name='manage-bookings-hotel'),
    path('manage-bookings/<int:hotel_id>/<int:room_id>/', manage_bookings, name='manage-bookings-room'),
    path('hotel/add/', HotelCreateView.as_view(), name='hotel-add'),
    path('hotel/<int:pk>/edit/', HotelUpdateView.as_view(), name='hotel-edit'),
    path('hotel/<int:pk>/delete/', HotelDeleteView.as_view(), name='hotel-delete'),
    path('hotel/<int:pk>/reviews/', HotelReviewsView.as_view(), name='hotel-reviews'),
    path('hotel/<int:pk>/room/add/', RoomCreateView.as_view(), name='room-add'),
    path('hotel/<int:pk>/room/<int:room_id>/edit/', RoomUpdateView.as_view(), name='room-edit'),
    path('hotel/<int:pk>/room/<int:room_id>/delete/', RoomDeleteView.as_view(), name='room-delete'),
    path('hotel/<int:pk>/room/<int:room_id>/availability/', RoomAvailabilityView.as_view(), name='room-availability'),
    path('reservations/', ReservationListView.as_view(), name='reservation-list'),
    path('bookings/', views.booking_list, name='booking-list'),
    path('bookings/<int:pk>/cancel/', views.cancel_booking, name='cancel-booking'),
    path('bookings/<int:pk>/edit/', views.edit_booking, name='edit-booking'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)