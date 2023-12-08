from django.shortcuts import render

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
    hotels = {
        'hotels': 'Roch Hotels|Hotels'
    }
    return render(request, 'main/hotels.html', hotels)