from django.urls import path
from . import views

urlpatterns = [
    path('', views.meal_plan_page, name='meal_plan_page'),
]