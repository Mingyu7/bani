from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import ChatRoom

User = get_user_model()

@login_required
def index(request):
    user = request.user
    # Find chat rooms where the user's ID is part of the name
    # Assumes room names are like 'trade_1-3', 'trade_5-1', etc.
    chat_rooms = ChatRoom.objects.filter(
        name__startswith='trade_',
    ).filter(
        Q(name__contains=f'_{user.id}-') | 
        Q(name__contains=f'-{user.id}')
    ).distinct()

    # Prepare a list with room and other user's info
    user_chats = []
    for room in chat_rooms:
        try:
            # Extract user IDs from the room name 'trade_A-B'
            ids_str = room.name.split('_')[1]
            user_id_1, user_id_2 = map(int, ids_str.split('-'))
            
            # Determine the other user's ID
            other_user_id = user_id_2 if user.id == user_id_1 else user_id_1
            
            # Get the other user's object
            other_user = User.objects.get(id=other_user_id)
            
            user_chats.append({
                'room': room,
                'other_user': other_user
            })
        except (IndexError, ValueError, User.DoesNotExist):
            # Skip rooms with malformed names or non-existent users
            continue

    return render(request, 'message/index.html', {'user_chats': user_chats})

@login_required
def room(request, room_name):
    return render(request, 'message/room.html', {
        'room_name': room_name,
        'nickname': request.user.nickname
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
