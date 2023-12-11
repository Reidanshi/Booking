from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('hotels/', views.hotels, name='hotels'),
    path('create/', views.create, name='create'),
    path('hotels/<int:pk>', views.HotelDetailView.as_view(), name='hotel-detail'),
    # path('hotels/<int:pk>/update', views.HotelUpdateView.as_view(), name='hotel-update'),
    path('hotels/<int:pk>/rooms/', views.RoomListView.as_view(), name='room-list'),
    # path('hotels/<int:pk>/rooms', views.RoomListView.as_view(), name='room-list'),
    path('hotels/<int:pk>/rooms/<int:room_id>', views.RoomDetailView.as_view(), name='room-detail'),
]