from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Count
from .models import Recipe, Category
