import json
import random
from django.shortcuts import render
from datetime import date, timedelta
from meal_plans.models import MealPlan, MealItem
from news.api import fetch_news

def get_daily_meal_for_widget():
    """
    새로운 모델 구조에서 오늘의 식단 정보를 가져와 위젯에 표시할 HTML을 생성합니다.
    """
    today = date.today()
    current_weekday_num = today.weekday() # 월요일=0
    start_of_week = today - timedelta(days=current_weekday_num)
    
    # 요일 숫자 -> 모델의 문자열 ('Mon', 'Tue'...)
    day_map_num_to_str = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    today_str = day_map_num_to_str.get(current_weekday_num)

    # 이번 주 식단 찾기
    meal_plan = MealPlan.objects.filter(week_start_date=start_of_week).first()
    if not meal_plan or not today_str:
        return "<p>오늘 식단 정보가 없습니다.</p>"

    # 오늘에 해당하는 식단 아이템들 찾기
    todays_meals = meal_plan.items.filter(day_of_week=today_str).order_by('meal_type')
    
    if not todays_meals:
        return "<p>오늘 식단 정보가 없습니다.</p>"

    content = ""
    for meal in todays_meals:
        menu_with_br = meal.menu.replace('\n', '<br>')
        content += f"<h6>[{meal.meal_type}]</h6><p>{menu_with_br}</p>"
    
    return content if content else "<p>오늘 식단 정보가 없습니다.</p>"


def index(request):
    # Fetch daily meal
    daily_meal = get_daily_meal_for_widget()

    # Prepare weather cities
    all_cities = [
        ('Seoul', '서울특별시'), ('Busan', '부산'), ('Daegu', '대구'), ('Incheon', '인천'),
        ('Gwangju', '광주'), ('Daejeon', '대전'), ('Ulsan', '울산'), ('Jeju', '제주'),
        ('Suwon', '수원'), ('Chuncheon', '춘천'), ('Cheongju', '청주'), ('Cheonan', '천안'),
        ('Jeonju', '전주'), ('Mokpo', '목포'), ('Pohang', '포항'), ('Changwon', '창원')
    ]
    cheonan = ('Cheonan', '천안')
    
    # Remove Cheonan to avoid duplication
    other_cities = [city for city in all_cities if city != cheonan]
    random.shuffle(other_cities)
    
    # Select Cheonan + 3 other random cities
    final_cities = [cheonan] + other_cities[:3]

    # Fetch random news article
    articles, error = fetch_news(page_size=50) # Fetch more articles to get a better random sample
    random_news_article = None
    if articles:
        random_news_article = random.choice(articles)

    context = {
        'daily_meal': daily_meal,
        'weather_cities': json.dumps(final_cities),
        'random_news_article': random_news_article,
    }
    return render(request, 'core/index.html', context)