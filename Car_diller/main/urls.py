from django.urls import path
from . import views


urlpatterns = [
    path('', views.info),
    path('about/', views.about),
    path('hotels/', views.hotels),
]