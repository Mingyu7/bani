from django.urls import path

from . import views

app_name = 'message'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_private_chat/<str:username>/', views.create_private_chat, name='create_private_chat'),
    path('<str:room_name>/', views.room, name='room'),
]
