from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    image = forms.ImageField(label='이미지', required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ['title', 'content', 'price', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '상품 제목을 입력하세요'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': '상품 설명을 입력하세요'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '가격을 입력하세요'}),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'price': '가격',
        }
