from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('check-username/', views.check_username, name='check-username'),
    path('profile/', views.profile_update_view, name='profile_update'),
]