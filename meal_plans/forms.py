from django import forms
from .models import DailyMeal

class DailyMealForm(forms.ModelForm):
    class Meta:
        model = DailyMeal
        fields = ['date', 'campus', 'meal_type', 'menu_text']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'campus': forms.Select(attrs={'class': 'form-control'}),
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'menu_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'date': '날짜',
            'campus': '캠퍼스',
            'meal_type': '식사 종류',
            'menu_text': '메뉴 (예: 백미밥 / 콩나물국 / ...)',
        }
