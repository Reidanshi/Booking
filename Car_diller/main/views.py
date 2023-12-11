from django.views.generic import UpdateView, DetailView, DeleteView
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Hotel, Room
from .serializers import HotelSerializer, RoomSerializer
from rest_framework.generics import ListAPIView
from django.views import View
from .forms import HotelForm, RoomForm



def home(request):
    date = {
        'title': 'Roch Hotels Official Site',
    }
    return render(request, 'main/main.html', date)

class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'main/details_view.html'
    context_object_name = 'hotels'


# class HotelUpdateView(UpdateView):
#     model = Hotel
#     template_name = 'main/create.html'
#     form_class = HotelForm

# class HotelDeleteView(DeleteView):
#     model = Hotel
#     success_url = '/hotels/'
#     template_name = 'main/hotels_delete.html'


def rooms(request):
    rooms= Room.objects.all()
    return render(request, 'main/room_list.html')

class RoomListView(DetailView):
    model = Room
    success_url = '/rooms/'
    template_name = 'main/room_list.html'

class RoomDetailView(DetailView):
    model = Room
    template_name = 'main/rooms_detail_view.html'
    context_object_name = 'room'

# class RoomViewSet(viewsets.ModelViewSet):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer


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
#


# class HotelViewSet(viewsets.ModelViewSet):
#     queryset = Hotel.objects.all()
#     serializer_class = HotelSerializer





# class ManageHotelView(View):
#     def get(self, request, *args, **kwargs):
#         hotels = Hotel.objects.all()
#         form = HotelForm()
#         return render(request, 'manage_hotel.html', {'hotels': hotels, 'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = HotelForm(request.POST)
#         if form.is_valid():
#             hotel_id = request.POST.get('hotel_id')
#             if hotel_id:
#                 hotel = Hotel.objects.get(id=hotel_id)
#                 form = HotelForm(request.POST, instance=hotel)
#             else:
#                 form.save()
#         return redirect('manage-hotel')
#
#     def get(self, request, *args, **kwargs):
#         hotel_id = request.GET.get('hotel_id')
#         if hotel_id:
#             Hotel.objects.get(id=hotel_id).delete()
#         return redirect('manage-hotel')
#
#
# class RoomListAPIView(ListAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#
# class HotelListAPIView(ListAPIView):
#     queryset = Hotel.objects.all()
#     serializer_class = HotelSerializer
#
#
# class ManageHotelView(View):
#     def get(self, request, *args, **kwargs):
#         hotels = Hotel.objects.all()
#         form = HotelForm()
#         return render(request, 'manage_hotel.html', {'hotels': hotels, 'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = HotelForm(request.POST)
#         if form.is_valid():
#             hotel_id = request.POST.get('hotel_id')
#             if hotel_id:
#                 hotel = Hotel.objects.get(id=hotel_id)
#                 form = HotelForm(request.POST, instance=hotel)
#             else:
#                 form.save()
#         return redirect('manage-hotel')
#
#     def get(self, request, *args, **kwargs):
#         hotel_id = request.GET.get('hotel_id')
#         if hotel_id:
#             Hotel.objects.get(id=hotel_id).delete()
#         return redirect('manage-hotel')  #
#
#
# class ManageRoomView(View):
#     def get(self, request, *args, **kwargs):
#         rooms = Room.objects.all()
#         form = RoomForm()
#         return render(request, 'manage_room.html', {'rooms': rooms, 'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = RoomForm(request.POST)
#         if form.is_valid():
#             new_room = form.save()
#             return redirect('manage-room')
#         rooms = Room.objects.all()
#         return render(request, 'manage_room.html', {'rooms': rooms, 'form': form})