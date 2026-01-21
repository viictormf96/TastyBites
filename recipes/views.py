from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.db.models import Count
from .models import Recipe, Category


class CategoriesDashboardView(ListView):
    model = Category
    context_object_name = "categories_list"
    template_name = "categories/categories.html"

    def get_queryset(self):
        return super().get_queryset().annotate(
            total_favorites = Count("recipe__favorites", distinct=True),
            total_recipes = Count("recipe", distinct=True)
        ).order_by("-total_recipes")