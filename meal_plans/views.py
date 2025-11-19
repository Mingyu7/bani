from django.shortcuts import render
from .models import MealPlan
from datetime import date, timedelta

def weekly_meal_plan_view(request):
    """
    이번 주 식단표를 조회하여 템플릿에 전달하는 뷰
    """
    today = date.today()
    # 오늘이 무슨 요일인지 확인 (월요일=0, 일요일=6)
    current_weekday = today.weekday()
    # 이번 주 월요일 날짜 계산
    start_of_week = today - timedelta(days=current_weekday)
    
    # 이번 주에 해당하는 식단표를 찾음
    meal_plan = MealPlan.objects.filter(week_start_date=start_of_week).first()
    
    # 템플릿에 전달할 데이터 구조
    # ex: {'중식': {'월': '메뉴', '화': '메뉴'}, '석식': ...}
    plan_data = {
        '중식': {},
        '석식': {}
    }
    
    if meal_plan:
        # 요일 이름 매핑 (모델의 'Mon' -> 템플릿의 '월')
        day_map = {
            'Mon': '월', 'Tue': '화', 'Wed': '수', 'Thu': '목', 'Fri': '금', 'Sat': '토', 'Sun': '일'
        }
        for item in meal_plan.items.all():
            # 모델에 저장된 'Mon', 'Tue' 등을 '월', '화' 로 변환
            day_in_korean = day_map.get(item.day_of_week, '')
            if day_in_korean and item.meal_type in plan_data:
                plan_data[item.meal_type][day_in_korean] = item.menu

    context = {
        'week_start_date': start_of_week,
        'week_end_date': start_of_week + timedelta(days=4), # 금요일까지
        'plan_data': plan_data,
        'days_of_week': ['월', '화', '수', '목', '금'],
    }
    
    return render(request, 'meal_plans/weekly_meal_plan.html', context)