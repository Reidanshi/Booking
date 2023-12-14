from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static
from .views import register, profile, manage_bookings
from .views import CustomLoginView, CustomLogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('hotels/', views.hotels, name='hotels'),
    path('create/', views.create, name='create'),
    path('hotels/<int:pk>', views.HotelDetailView.as_view(), name='hotel-detail'),
    path('hotels/<int:pk>/rooms/', views.RoomListView.as_view(), name='room-list'),
    path('hotels/<int:pk>/rooms/<int:room_id>', views.RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:pk>/book/<int:room_id>/', views.book_room, name='book-room'),
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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)