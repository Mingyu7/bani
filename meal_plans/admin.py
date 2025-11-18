from django.contrib import admin
from .models import MealPlan, MealItem

class MealItemInline(admin.TabularInline):
    model = MealItem
    extra = 1  # 기본으로 보여줄 추가 입력 폼의 수
    fields = ['day_of_week', 'meal_type', 'menu']
    ordering = ['day_of_week', 'meal_type']

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('week_start_date', 'created_at')
    inlines = [MealItemInline]

@admin.register(MealItem)
class MealItemAdmin(admin.ModelAdmin):
    list_display = ('meal_plan', 'day_of_week', 'meal_type', 'menu_summary')
    list_filter = ('meal_plan__week_start_date', 'day_of_week', 'meal_type')
    search_fields = ('menu',)

    def menu_summary(self, obj):
        return obj.menu[:50] + '...' if len(obj.menu) > 50 else obj.menu
    menu_summary.short_description = '메뉴 미리보기'
