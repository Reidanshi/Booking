from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static
from .views import register, profile, manage_bookings, cancel_booking, view_reviews
from .views import CustomLoginView, CustomLogoutView, hotel_detail, add_review


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('hotels/', views.hotels, name='hotels'),
    path('create/', views.create, name='create'),
    path('hotels/<int:pk>/', hotel_detail, name='hotel-detail'),
    path('hotels/<int:hotel_id>/add-review/', add_review, name='add-review'),
    path('my-reviews/<int:pk>/', view_reviews, name='view-reviews'),
    # path('reviews/<int:pk>/update/', views.update_review, name='update-review'),
    # path('reviews/<int:pk>/delete/', views.delete_review, name='delete-review'),
    path('hotels/<int:pk>/rooms/', views.RoomListView.as_view(), name='room-list'),
    path('hotels/<int:pk>/rooms/<int:room_id>', views.RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:pk>/book/<int:room_id>/', views.book_room, name='book-room'),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel-booking'),
    path('register/', register, name='register'),
    path('change-password/', PasswordChangeView.as_view(template_name='main/change_password.html'), name='change-password'),
    path('change-password/done/', PasswordChangeDoneView.as_view(template_name='main/change_password_done.html'), name='change-password-done'),
    path('reset-password/', PasswordResetView.as_view(template_name='main/reset_password.html'), name='reset-password'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='main/reset_password_done.html'), name='reset-password-done'),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='main/reset_password_confirm.html'), name='reset-password-confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name='main/reset_password_complete.html'), name='reset-password-complete'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('manage-bookings/', manage_bookings, name='manage-bookings'),
    path('manage-bookings/<int:hotel_id>/', manage_bookings, name='manage-bookings-hotel'),
    path('manage-bookings/<int:hotel_id>/<int:room_id>/', manage_bookings, name='manage-bookings-room'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)