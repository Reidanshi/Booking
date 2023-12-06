from django.shortcuts import render

def info(request):
    return render(request, 'main/main.html')


def about(request):
    return render(request, 'main/about.html')


def hotels(request):
    return render(request, 'main/hotels.html')