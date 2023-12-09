from django.shortcuts import render
from .models import Hotel
from .forms import HotelForm


def home(request):
    date = {
        'title': 'Roch Hotels Official Site',
    }
    return render(request, 'main/main.html', date)


def about(request):
    about = {
        'about': 'Roch Hotels|Info',
    }
    return render(request, 'main/about.html', about)


def hotels(request):
    hotels = Hotel.objects.order_by('location')

    return render(request, 'main/hotels.html', {'hotels':hotels})

def create(request):
    form =HotelForm()

    date = {
        'form': form
    }

    return render(request, 'main/create.html', date)