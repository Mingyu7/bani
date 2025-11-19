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

class FindPasswordForm(forms.Form):
    username = forms.CharField(label="아이디", max_length=150)
    email = forms.EmailField(label="이메일")
    new_password1 = forms.CharField(label="새 비밀번호", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="새 비밀번호 확인", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("두 비밀번호가 일치하지 않습니다.")
        
        return cleaned_data

