from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib import messages
from .models import ChatRoom

User = get_user_model()

@login_required
def index(request):
    user = request.user
    # Find chat rooms for trade or dating where the user is a participant
    chat_rooms = ChatRoom.objects.filter(
        Q(name__startswith='trade_') | Q(name__startswith='dating_')
    ).filter(
        Q(name__contains=f'-{user.id}') | Q(name__contains=f'_{user.id}-') # Adjusted to find ID with separators
    ).distinct()

    user_chats = []
    for room in chat_rooms:
        try:
            # Extract prefix and user IDs from the room name 'prefix_A-B'
            parts = room.name.split('_')
            prefix = parts[0]
            ids_str = parts[1]
            user_id_1, user_id_2 = map(int, ids_str.split('-'))
            
            other_user_id = user_id_2 if user.id == user_id_1 else user_id_1
            other_user = User.objects.get(id=other_user_id)
            
            # Create a user-friendly title based on the prefix
            chat_title = f"{other_user.nickname}님과의 대화"
            if prefix == 'trade':
                chat_title = f"[중고거래] {chat_title}"
            elif prefix == 'dating':
                chat_title = f"[데이팅] {chat_title}"

            user_chats.append({
                'room': room,
                'other_user': other_user,
                'chat_title': chat_title,
            })
        except (IndexError, ValueError, User.DoesNotExist):
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
    
    # Create a unique room name for the two users with a prefix
    if request.user.id > other_user.id:
        room_name = f'dating_{other_user.id}-{request.user.id}'
    else:
        room_name = f'dating_{request.user.id}-{other_user.id}'

    return redirect('message:room', room_name=room_name)

@require_POST
@login_required
def delete_chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    user = request.user

    # Security check: Ensure the user is a participant of the room
    try:
        ids_str = room.name.split('_')[1]
        user_ids = [int(uid) for uid in ids_str.split('-')]
        if user.id not in user_ids:
            messages.error(request, '채팅방을 삭제할 권한이 없습니다.')
            return redirect('message:index')
    except (IndexError, ValueError):
        messages.error(request, '잘못된 형식의 채팅방입니다.')
        return redirect('message:index')

    room.delete()
    messages.success(request, f'"{room.name}" 채팅방이 삭제되었습니다.')
    return redirect('message:index')
