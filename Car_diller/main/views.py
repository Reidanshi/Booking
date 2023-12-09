from django.shortcuts import render, redirect
from .models import Hotel
from .forms import HotelForm
from django.views.generic import UpdateView, DetailView, DeleteView

def home(request):
    date = {
        'title': 'Roch Hotels Official Site',
    }
    return render(request, 'main/main.html', date)

class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'main/details_view.html'
    context_object_name = 'hotels'


class HotelUpdateView(UpdateView):
    model = Hotel
    template_name = 'main/create.html'

    form_class = HotelForm

class HotelDeleteView(DeleteView):
    model = Hotel
    success_url = '/hotels/'
    template_name = 'main/hotels_delete.html'


def about(request):
    about = {
        'about': 'Roch Hotels|Info',
    }
    return render(request, 'main/about.html', about)


def hotels(request):
    hotels = Hotel.objects.order_by('location')

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