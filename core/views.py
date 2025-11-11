import json
from django.shortcuts import render
from meal_plans.views import get_daily_meal # meal_plans 앱의 get_daily_meal 함수 임포트

def index(request):
    daily_meal = get_daily_meal()
    cities = [
        ('Seoul', '서울특별시'), ('Busan', '부산'), ('Daegu', '대구'), ('Incheon', '인천'),
        ('Gwangju', '광주'), ('Daejeon', '대전'), ('Ulsan', '울산'), ('Jeju', '제주'),
        ('Suwon', '수원'), ('Chuncheon', '춘천'), ('Cheongju', '청주'), ('Cheonan', '천안'),
        ('Jeonju', '전주'), ('Mokpo', '목포'), ('Pohang', '포항'), ('Changwon', '창원')
    ]
    context = {
        'daily_meal': daily_meal,
        'weather_cities': json.dumps(cities),
    }
    return render(request, 'core/index.html', context)