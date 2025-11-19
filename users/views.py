from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, FindPasswordForm
from django.http import JsonResponse
from .models import User
from django.contrib import messages

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'

def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def find_password(request):
    # SECURITY WARNING: This is an insecure way to reset passwords.
    # It should not be used in a production environment.
    if request.method == 'POST':
        form = FindPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password1']

            try:
                user = User.objects.get(username=username, email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, '비밀번호가 성공적으로 변경되었습니다. 새 비밀번호로 로그인하세요.')
                return redirect('users:login')
            except User.DoesNotExist:
                messages.error(request, '해당 아이디와 이메일 주소를 가진 사용자를 찾을 수 없습니다.')
    else:
        form = FindPasswordForm()

    return render(request, 'users/find_password.html', {'form': form})