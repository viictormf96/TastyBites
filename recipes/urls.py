from django.urls import path
from .views import CategoriesDashboardView



app_name="recipes"

urlpatterns = [
    path("categories/", CategoriesDashboardView.as_view(), name="categories"),
]