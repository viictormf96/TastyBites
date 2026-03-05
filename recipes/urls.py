from django.urls import path
from .views import CategoriesDashboardView, RecipesDashboardView, CategoryDashboardView
from . import views



app_name="recipes"

urlpatterns = [
    path("categories/", CategoriesDashboardView.as_view(), name="categories"),
    path("recipes/", RecipesDashboardView.as_view(), name="recipes"),
    path("category/<slug:slug_category>", CategoryDashboardView.as_view(), name="category"),
]