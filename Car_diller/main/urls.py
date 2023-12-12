from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('hotels/', views.hotels, name='hotels'),
    path('create/', views.create, name='create'),
    path('hotels/<int:pk>', views.HotelDetailView.as_view(), name='hotel-detail'),
    path('hotels/<int:pk>/rooms/', views.RoomListView.as_view(), name='room-list'),
    path('hotels/<int:pk>/rooms/<int:room_id>', views.RoomDetailView.as_view(), name='room-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)