from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, FindPasswordForm, CustomSetPasswordForm, ProfileUpdateForm
from django.http import JsonResponse
from .models import User
from django.contrib import messages

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('mypage:mypage')

    def get_object(self, queryset=None):
        # Ensure the user can only edit their own profile
        return self.request.user

def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def find_password(request):
    if request.method == 'POST':
        form = FindPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(username=username, email=email)
                # Store user's ID in session to verify in the next step
                request.session['user_id_for_password_reset'] = user.id
                return redirect('users:reset_password_confirm')
            except User.DoesNotExist:
                messages.error(request, '해당 아이디와 이메일 주소를 가진 사용자를 찾을 수 없습니다.')
    else:
        form = FindPasswordForm()

    return render(request, 'users/find_password.html', {'form': form})

def reset_password_confirm(request):
    user_id = request.session.get('user_id_for_password_reset')
    if not user_id:
        messages.error(request, '비밀번호 재설정 세션이 만료되었거나 잘못된 접근입니다. 다시 시도해주세요.')
        return redirect('users:find_password')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, '사용자를 찾을 수 없습니다.')
        return redirect('users:find_password')

    if request.method == 'POST':
        form = CustomSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            # Clean up the session
            del request.session['user_id_for_password_reset']
            messages.success(request, '비밀번호가 성공적으로 변경되었습니다. 새 비밀번호로 로그인하세요.')
            return redirect('users:login')
    else:
        form = CustomSetPasswordForm(user)

    return render(request, 'users/reset_password_confirm.html', {'form': form})