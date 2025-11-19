from django.urls import path
from . import views

app_name = 'meal_plans'

urlpatterns = [
    path('', views.weekly_meal_plan_view, name='meal_plan_page'),
    path('admin/meal-plan/', views.meal_plan_admin_view, name='meal_plan_admin'),
    path('admin/meal-plan/edit/<int:pk>/', views.meal_plan_admin_view, name='meal_plan_admin_edit'),
]