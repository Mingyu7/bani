from django.urls import path
from . import views

app_name = 'dating'

urlpatterns = [
    path('', views.dating_page, name='dating_page'),
]
