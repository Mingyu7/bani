from django.db import models
from users.models import User
from board.models import Category

class Product(models.Model):
    id = models.AutoField(primary_key=True)  # 매물 PK
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')  # 판매자 (FK)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')  # 카테고리 (FK)
    title = models.CharField(max_length=200)  # 제목
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # 상품 이미지
    location = models.CharField(max_length=100, blank=True, null=True)  # 거래 지역
    description = models.TextField(blank=True, null=True)  # 설명
    price = models.IntegerField()  # 가격
    status = models.CharField(max_length=20, default='sale')  # 상태 ('sale', 'reserved', 'sold')
    created_at = models.DateTimeField(auto_now_add=True)  # 등록일시

    def __str__(self):
        return self.title


class Favorite(models.Model):
    id = models.AutoField(primary_key=True)  # 찜 PK
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')  # 찜한 유저 (FK)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')  # 찜한 상품 (FK)
    created_at = models.DateTimeField(auto_now_add=True)  # 찜한 시각

    class Meta:
        unique_together = ('user', 'product')  # 유저-상품 중복 방지

    def __str__(self):
        return f"{self.user.nickname} ❤️ {self.product.title}"


class ChatRoom(models.Model):
    id = models.AutoField(primary_key=True)  # 채팅방 PK
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chatrooms')  # 상품 ID (FK)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_chatrooms')  # 판매자 ID (FK)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_chatrooms')  # 구매자 ID (FK)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일시

    def __str__(self):
        return f"ChatRoom: {self.product.title}"


class Message(models.Model):
    id = models.AutoField(primary_key=True)  # 메시지 PK
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')  # 채팅방 ID (FK)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')  # 보낸 사람 (FK)
    content = models.TextField()  # 메시지 내용
    sent_at = models.DateTimeField(auto_now_add=True)  # 보낸 시간
    is_read = models.BooleanField(default=False)  # 읽음 여부

    def __str__(self):
        return f"{self.sender.nickname}: {self.content[:20]}"
