from django.conf import settings
from django.db import models
from users.models import User
from .utils import product_image_upload_path
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
import io

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

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            img = ImageOps.exif_transpose(img)  # Correct orientation
            # Resize image if it's too large
            if img.height > 1024 or img.width > 1024:
                output_size = (1024, 1024)
                img.thumbnail(output_size)

            # Save the image to a BytesIO object
            img_io = io.BytesIO()
            img_format = 'JPEG' if self.image.name.lower().endswith('jpg') or self.image.name.lower().endswith('jpeg') else 'PNG'
            img.save(img_io, format=img_format, quality=85, optimize=True)
            
            # Create a new Django file-like object
            new_image = ContentFile(img_io.getvalue(), name=self.image.name)
            self.image = new_image

        super().save(*args, **kwargs)