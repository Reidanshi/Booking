# from rest_framework.routers import DefaultRouter
# from .api import UserViewSet, HotelViewSet, RoomViewSet, BookingViewSet, ReviewViewSet
# from django.urls import path
# from . import views
# from .views import register, register_admin, profile, manage_bookings, cancel_booking, view_reviews
# from .views import CustomLoginView, custom_logout, hotel_detail, add_review, update_hotel, add_room, edit_room
# from .views import delete_hotel, manage_rooms, delete_room, update_reviews, delete_reviews, my_reviews, delete_reviews_admin
# from .views import manage_bookings_admin, view_reviews_admin, my_hotel, register_hotel, info_room, update_reviews_admin
# from django.conf.urls.static import static
# from django.conf import settings
#
#
# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'hotels', HotelViewSet)
# router.register(r'rooms', RoomViewSet)
# router.register(r'bookings', BookingViewSet)
# router.register(r'reviews', ReviewViewSet)
#
# urlpatterns = [
#     path('', views.home, name='home'),
#     path('hotels/', views.hotels, name='hotels'),
#     path('hotels/<int:pk>/', hotel_detail, name='hotel-detail'),
#     path('hotels/<int:pk>/rooms/', views.RoomListView.as_view(), name='room-list'),
#     path('hotels/<int:pk>/rooms/<int:room_id>', views.RoomDetailView.as_view(), name='room-detail'),
#     path('register/', register, name='register'),
#     path('register/admin/', register_admin, name='register_admin'),
#     path('accounts/profile/', profile, name='profile'),
#     path('accounts/login/', CustomLoginView.as_view(), name='login'),
#     path('accounts/logout/', custom_logout, name='logout'),
#     path('register-hotel/', register_hotel, name='register-hotel'),
#     path('my-hotel/', my_hotel, name='my-hotel'),
#     path('edit-hotel/<int:pk>/', update_hotel, name='edit-hotel'),
#     path('delete-hotel/<int:pk>/', delete_hotel, name='delete-hotel'),
#     path('manage-rooms/<int:pk>/', manage_rooms, name='manage-rooms'),
#     path('add-room/<int:pk>/', add_room, name='add-room'),
#     path('info-room/<int:pk>/', info_room, name='info-room'),
#     path('delete-room/<int:pk>/', delete_room, name='delete-room'),
#     path('edit-room/<int:pk>/', edit_room, name='edit-room'),
#     path('hotels/<int:pk>/rooms/<int:room_id>/book/', views.book_room, name='book-room'),
#     path('manage-bookings/', manage_bookings, name='manage-bookings'),
#     path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel-booking'),
#     path('manage-bookings-admin/', manage_bookings_admin, name='manage-bookings-admin'),
#     path('approve-booking/<int:booking_id>/', views.approve_booking, name='approve-booking'),
#     path('reject-booking/<int:booking_id>/', views.reject_booking, name='reject-booking'),
#     path('hotels/<int:hotel_id>/add-review/', add_review, name='add-review'),
#     path('view-reviews/<int:pk>/', view_reviews, name='view-reviews'),
#     path('my-reviews/', my_reviews, name='my-reviews'),
#     path('update-reviews/<int:review_id>/', update_reviews, name='update-reviews'),
#     path('delete-reviews/<int:review_id>/', delete_reviews, name='delete-reviews'),
#     path('view-reviews-admin/', view_reviews_admin, name='view-reviews-admin'),
#     path('update-reviews-admin/<int:review_id>/', update_reviews_admin, name='update-reviews-admin'),
#     path('delete-reviews-admin/<int:review_id>/', delete_reviews_admin, name='delete-reviews-admin'),
# ]
#
# urlpatterns += router.urls
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)