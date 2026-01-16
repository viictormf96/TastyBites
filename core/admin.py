from django.contrib import admin
from .models import  Favorite, Comment 
# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    list_display = ("recipe", "user", "created_at")
    search_fields = ("name", "user", "recipe")

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    search_fields = ("user", "recipe")