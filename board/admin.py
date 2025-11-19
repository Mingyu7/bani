from django.contrib import admin
from .models import Post, Comment, Category

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at', 'content')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content')

admin.site.register(Post)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)