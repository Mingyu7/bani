from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

@login_required
def index(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'message/index.html', {'users': users})

@login_required
def room(request, room_name):
    return render(request, 'message/room.html', {
        'room_name': room_name,
        'username': request.user.username
    })

@login_required
def create_private_chat(request, username):
    other_user = User.objects.get(username=username)
    
    # Create a unique room name for the two users
    if request.user.id > other_user.id:
        room_name = f'{request.user.id}_{other_user.id}'
    else:
        room_name = f'{other_user.id}_{request.user.id}'

    return redirect('room', room_name=room_name)
