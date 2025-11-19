from django.conf import settings
from django.db import models
from users.models import User
from .utils import product_image_upload_path # Import the custom upload path function

class Product(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to=product_image_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    wishlisted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='wishlist', blank=True)

    def __str__(self):
        return self.title