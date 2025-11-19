from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('check-username/', views.check_username, name='check-username'),
    path('find_password/', views.find_password, name='find_password'),
    path('reset_password_confirm/', views.reset_password_confirm, name='reset_password_confirm'),

    # Login and Logout
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]