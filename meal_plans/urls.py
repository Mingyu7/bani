from django.urls import path
from . import views

app_name = 'meal_plans'

urlpatterns = [
    path('', views.meal_plan_page, name='meal_plan_page'),
]