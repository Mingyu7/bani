from django.db import models

class MealPlan(models.Model):
    id = models.AutoField(primary_key=True)  # 식단표 PK
    week_start_date = models.DateField()  # 해당 주의 시작 날짜 (월요일 기준)
    created_at = models.DateTimeField(auto_now_add=True)  # 등록일

    def __str__(self):
        return f"Meal Plan - {self.week_start_date}"


class MealItem(models.Model):
    id = models.AutoField(primary_key=True)  # 식단 아이템 PK
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='items')  # 소속 식단표 (FK)
    day_of_week = models.CharField(max_length=10)  # 요일 (Mon, Tue, Wed, Thu, Fri, Sat, Sun)
    meal_type = models.CharField(max_length=10)  # 식사 구분 (중식, 석식)
    menu = models.TextField()  # 해당 식단 메뉴

    def __str__(self):
        return f"{self.day_of_week} {self.meal_type}: {self.menu[:15]}"
