from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import DailyMeal
from .forms import DailyMealForm
from datetime import date, timedelta

def weekly_meal_plan_view(request):
    """
    이번 주 식단표를 조회하여 템플릿에 전달하는 뷰
    """
    today = date.today()
    current_weekday = today.weekday()  # 월요일=0, 일요일=6
    start_of_week = today - timedelta(days=current_weekday)
    end_of_week = start_of_week + timedelta(days=6)

    selected_campus = request.GET.get('campus', '아산') # Default to 아산

    # Fetch DailyMeal entries for the current week and selected campus
    daily_meals_this_week = DailyMeal.objects.filter(
        date__range=[start_of_week, end_of_week],
        campus=selected_campus
    ).order_by('date', 'meal_type')

    # Structure the data for the template
    plan_data = {}
    campus_choices = DailyMeal.CAMPUS_CHOICES
    
    # Initialize plan_data for selected campus
    plan_data[selected_campus] = {}
    for i in range(7): # For each day of the week
        day = start_of_week + timedelta(days=i)
        day_korean = ['월', '화', '수', '목', '금', '토', '일'][i]
        plan_data[selected_campus][day_korean] = {
            'date': day,
            '중식': '정보 없음',
            '석식': '정보 없음',
        }

    for meal in daily_meals_this_week:
        day_korean = ['월', '화', '수', '목', '금', '토', '일'][meal.date.weekday()]
        if meal.meal_type == '중식':
            plan_data[selected_campus][day_korean]['중식'] = meal.menu_text
        elif meal.meal_type == '석식':
            plan_data[selected_campus][day_korean]['석식'] = meal.menu_text

    context = {
        'week_start_date': start_of_week,
        'week_end_date': end_of_week,
        'plan_data': plan_data,
        'days_of_week': ['월', '화', '수', '목', '금', '토', '일'],
        'meal_types': ['중식', '석식'],
        'campus_choices': campus_choices,
        'selected_campus': selected_campus,
    }
    
    return render(request, 'meal_plans/weekly_meal_plan.html', context)


@staff_member_required
def meal_plan_admin_view(request, pk=None):
    if pk:
        daily_meal = get_object_or_404(DailyMeal, pk=pk)
    else:
        daily_meal = None

    if request.method == 'POST':
        form = DailyMealForm(request.POST, instance=daily_meal)
        if form.is_valid():
            form.save()
            return redirect('meal_plans:meal_plan_admin') # Redirect to the admin page itself
    else:
        form = DailyMealForm(instance=daily_meal)
    
    daily_meals = DailyMeal.objects.all() # Get all existing daily meals
    
    context = {
        'form': form,
        'daily_meals': daily_meals,
        'editing': daily_meal is not None,
    }
    return render(request, 'meal_plans/meal_plan_admin.html', context)