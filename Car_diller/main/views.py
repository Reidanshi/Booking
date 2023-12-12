from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect
from .models import Hotel, Room
from .forms import HotelForm



def home(request):
    date = {
        'title': 'Roch Hotels Official Site',
    }
    return render(request, 'main/main.html', date)

class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'main/details_view.html'
    context_object_name = 'hotels'


def room_list(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    rooms = Room.objects.filter(hotel=hotel, available=True)
    return render(request, 'main/room_list.html', {'hotel': hotel, 'rooms': rooms})

class RoomListView(ListView):
    model = Room
    template_name = 'main/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return Room.objects.filter(available=True)

class RoomDetailView(DetailView):
    model = Room
    template_name = 'main/rooms_detail_view.html'
    context_object_name = 'room'

    def get_object(self, queryset=None):
        hotel_id = self.kwargs['pk']
        room_id = self.kwargs['room_id']
        return Room.objects.get(hotel_id=hotel_id, id=room_id)

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
