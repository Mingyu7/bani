from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

GENDER_CHOICES = [
    ('M', '남성'),
    ('F', '여성'),
]

REGION_CHOICES = [
    ('서울', '서울'),
    ('부산', '부산'),
    ('대구', '대구'),
    ('인천', '인천'),
    ('광주', '광주'),
    ('대전', '대전'),
    ('울산', '울산'),
    ('세종', '세종'),
    ('경기도', '경기도'),
    ('강원도', '강원도'),
    ('충청북도', '충청북도'),
    ('충청남도', '충청남도'),
    ('전라북도', '전라북도'),
    ('전라남도', '전라남도'),
    ('경상북도', '경상북도'),
    ('경상남도', '경상남도'),
    ('제주도', '제주도'),
]

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="이메일",
        required=True,
    )
    nickname = forms.CharField(
        label="닉네임",
        required=True,
    )
    gender = forms.ChoiceField(
        label="성별",
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    region = forms.ChoiceField(
        label="지역",
        choices=REGION_CHOICES,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'nickname', 'gender', 'region')
        labels = {
            'username': '아이디',
        }

