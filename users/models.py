from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)  # 사용자 PK
    username = models.CharField(max_length=100, unique=True)  # 로그인 아이디
    password = models.CharField(max_length=255)  # 비밀번호
    email = models.EmailField(unique=True)  # 이메일
    nickname = models.CharField(max_length=100, unique=True)  # 닉네임 (고유)
    gender = models.CharField(max_length=1, blank=True, null=True)  # 성별 필드
    region = models.CharField(max_length=100, blank=True, null=True)  # 지역
    rating = models.FloatField(default=0.0)  # 평점
    profile_image = models.CharField(max_length=255, blank=True, null=True)  # 프로필 이미지 경로
    created_at = models.DateTimeField(auto_now_add=True)  # 가입일시

    def __str__(self):
        return self.nickname