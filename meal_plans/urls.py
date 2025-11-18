from django.urls import path
from . import views

app_name = 'meal_plans'

urlpatterns = [
    path('', views.weekly_meal_plan_view, name='meal_plan_page'),
]