from django.contrib import admin
from .models import Category, Subcategory, Recipe, Difficulty, Instruction, Ingredient,Comment,Favorite,Follower


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    list_display = ("name", "created_at")
    search_fields = ("name", "description")

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name", "category")

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    list_display = ("name", "user", "created_at")
    search_fields = ("name", "user", "description")

@admin.register(Difficulty)
class DifficultyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ("recipe", "step_number")
    search_fields = ("recipe",)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "recipe")
    search_fields = ("name", "recipe")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    list_display = ("recipe", "user", "created_at")
    search_fields = ("name", "user", "recipe")

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    search_fields = ("user", "recipe")

@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ("follower", "followee")
    search_fields = ("follower", "followee")

