from django.urls import path
from .views import CategoriesDashboardView, RecipesDashboardView
from . import views



app_name="recipes"

urlpatterns = [
    path("categories/", CategoriesDashboardView.as_view(), name="categories"),
    path("categories/search/", views.search_categories, name="search_categories"),
    path("recipes/", RecipesDashboardView.as_view(), name="recipes"),
]