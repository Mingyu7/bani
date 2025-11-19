from django.urls import path

from . import views

app_name = 'message'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_private_chat/<str:username>/', views.create_private_chat, name='create_private_chat'),
    path('delete/<int:room_id>/', views.delete_chat_room, name='delete_chat_room'),
    path('<str:room_name>/', views.room, name='room'),
]
