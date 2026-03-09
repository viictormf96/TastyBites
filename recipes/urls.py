from django.urls import path
from .views import CategoriesDashboardView, RecipesDashboardView, CategoryDashboardView, RecipeDashboardView
from . import views



app_name="recipes"

urlpatterns = [
    path("categories/", CategoriesDashboardView.as_view(), name="categories"),
    path("category/<slug:slug_category>", CategoryDashboardView.as_view(), name="category"),
    path("recipes/", RecipesDashboardView.as_view(), name="recipes"),
    path("recipe/<slug:slug_recipe>", RecipeDashboardView.as_view(), name="recipe"),
]