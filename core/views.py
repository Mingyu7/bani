import json
import random
from django.shortcuts import render
from datetime import date, timedelta
from meal_plans.models import DailyMeal # Import the new DailyMeal model
from news.api import fetch_news
from board.models import Post # Import Post model
from trade.models import Product # Import Product model

def index(request):
    today = date.today()
    today_meal_plans = {}

    campuses = ['아산'] # Only display Asan campus meal plan on the main page
    meal_types = ['중식', '석식']

    for campus in campuses:
        today_meal_plans[campus] = {}
        for meal_type in meal_types:
            meal_entry = DailyMeal.objects.filter(
                date=today,
                campus=campus,
                meal_type=meal_type
            ).first()
            if meal_entry:
                menu_items = meal_entry.menu_text.split('/')
                truncated_menu = '/'.join(menu_items[:5])
                today_meal_plans[campus][meal_type] = truncated_menu
            else:
                today_meal_plans[campus][meal_type] = '정보 없음'    
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

    # Fetch latest 5 posts from board
    latest_posts = Post.objects.order_by('-created_at')[:5]

    # Fetch latest 5 products from market
    latest_products = Product.objects.order_by('-created_at')[:5]

    context = {
        'today': today, # Pass today's date to the template
        'today_meal_plans': today_meal_plans,
        'weather_cities': json.dumps(final_cities),
        'random_news_article': random_news_article,
        'latest_posts': latest_posts,
        'latest_products': latest_products,
    }
    return render(request, 'core/index.html', context)