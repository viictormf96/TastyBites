from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.db.models import Count
from .models import Recipe, Category


class CategoriesDashboardView(TemplateView):
    template_name = "categories/categories.html"