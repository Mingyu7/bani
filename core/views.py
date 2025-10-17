from django.shortcuts import render
from meal_plans.views import get_daily_meal # meal_plans 앱의 get_daily_meal 함수 임포트

def index(request):
    daily_meal = get_daily_meal()
    context = {
        'daily_meal': daily_meal,
    }
    return render(request, 'core/index.html', context)