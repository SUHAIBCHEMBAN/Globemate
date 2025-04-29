from django.contrib import admin
from .models import (
    Category,
    Post,
    Comment,
    Like,    
)
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )    

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'author', 'created_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    

class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')     


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
