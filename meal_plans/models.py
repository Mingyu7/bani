from django.db import models

class MealPlan(models.Model):
    id = models.AutoField(primary_key=True)  # 식단표 PK
    week_start_date = models.DateField(unique=True, help_text="해당 주의 시작 날짜 (월요일 기준)")
    created_at = models.DateTimeField(auto_now_add=True)  # 등록일

    def __str__(self):
        return f"Meal Plan - {self.week_start_date}"


class MealItem(models.Model):
    DAY_OF_WEEK_CHOICES = [
        ('Mon', '월요일'),
        ('Tue', '화요일'),
        ('Wed', '수요일'),
        ('Thu', '목요일'),
        ('Fri', '금요일'),
        ('Sat', '토요일'),
        ('Sun', '일요일'),
    ]
    MEAL_TYPE_CHOICES = [
        ('중식', '중식'),
        ('석식', '석식'),
    ]

    id = models.AutoField(primary_key=True)  # 식단 아이템 PK
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='items')  # 소속 식단표 (FK)
    day_of_week = models.CharField(max_length=3, choices=DAY_OF_WEEK_CHOICES)  # 요일
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES)  # 식사 구분
    menu = models.TextField()  # 해당 식단 메뉴

    class Meta:
        unique_together = ('meal_plan', 'day_of_week', 'meal_type')

    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.meal_type}: {self.menu[:15]}"

class DailyMeal(models.Model):
    CAMPUS_CHOICES = [
        ('아산', '아산'),
        ('영동', '영동'),
    ]
    MEAL_TYPE_CHOICES = [
        ('중식', '중식'),
        ('석식', '석식'),
    ]
    
    campus = models.CharField(max_length=20, choices=CAMPUS_CHOICES)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES)
    date = models.DateField()
    menu_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('campus', 'meal_type', 'date')
        ordering = ['date', 'campus', 'meal_type']

    def __str__(self):
        return f"{self.date} - {self.campus} {self.meal_type}: {self.menu_text[:30]}..."
