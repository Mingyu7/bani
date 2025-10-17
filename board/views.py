from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'board/post_list.html', {'posts': posts})