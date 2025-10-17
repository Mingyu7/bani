from django.shortcuts import render
import datetime
from bs4 import BeautifulSoup
from django.conf import settings
import os

def get_daily_meal():
    try:
        # 요일 맵 (0:월, 1:화, ...)
        weekday_map = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        today_weekday = datetime.datetime.today().weekday()

        # 토/일요일은 식단 정보 없음 처리
        if today_weekday > 4: 
            return "<p>오늘은 식단 정보가 없습니다.</p>"

        today_str = weekday_map[today_weekday]

        # 식단표 파일 읽기
        file_path = os.path.join(settings.BASE_DIR, 'core', 'templates', 'core', 'components', 'meal-plan.html')
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # 테이블 헤더에서 오늘 요일의 인덱스 찾기
        headers = soup.find('thead').find_all('th')
        col_idx = -1
        for i, th in enumerate(headers):
            if today_str in th.text:
                col_idx = i
                break
        
        if col_idx == -1:
            return "<p>식단 정보를 찾을 수 없습니다.</p>"

        # 해당 인덱스의 중식, 석식 정보 가져오기
        lunch_menu = soup.select_one(f'tbody tr:nth-of-type(1) td:nth-of-type({col_idx})').decode_contents()
        dinner_menu = soup.select_one(f'tbody tr:nth-of-type(2) td:nth-of-type({col_idx-1})').decode_contents()

        return f'<h6>[중식]</h6><p>{lunch_menu}</p><h6>[석식]</h6><p>{dinner_menu}</p>'

    except Exception as e:
        return f"<p>식단 정보를 불러오는 중 오류가 발생했습니다.</p><p style='font-size:0.7rem; color:grey;'>{e}</p>"

def meal_plan_page(request):
    return render(request, 'meal_plans/weekly_meal_plan.html')