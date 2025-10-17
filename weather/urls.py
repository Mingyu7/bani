from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_page, name='weather_page'),
]