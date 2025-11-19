from django.db import models
from users.models import User

class Category(models.Model):
    id = models.AutoField(primary_key=True)  # 카테고리 PK
    name = models.CharField(max_length=100)  # 카테고리 이름
    type = models.CharField(max_length=20)  # 'product' 또는 'post'

    def __str__(self):
        return f"{self.name} ({self.type})"


class Post(models.Model):
    id = models.AutoField(primary_key=True)  # 게시글 PK
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # 작성자 (FK)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')  # 게시판 카테고리 (FK)
    title = models.CharField(max_length=200)  # 제목
    content = models.TextField()  # 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일시
    views = models.IntegerField(default=0)  # 조회수
    is_pinned_notice = models.BooleanField(default=False)  # 관리자 고정 공지 여부

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.AutoField(primary_key=True)  # 댓글 PK
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # 게시글 ID (FK)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # 작성자 (FK)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')  # 부모 댓글 (대댓글용)
    content = models.TextField()  # 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일시

    def __str__(self):
        return f"{self.user.nickname}: {self.content[:20]}"
