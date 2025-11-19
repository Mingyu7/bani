from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User
from .forms import CustomUserCreationForm, ProfileUpdateForm


@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 성공적으로 업데이트되었습니다.')
            return redirect('mypage:mypage')
    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'users/profile_update.html', context)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
