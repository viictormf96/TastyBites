from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.db.models import Count
from .models import Recipe, Category

#Categories seeker
def search_categories(request):
    query = request.GET.get('q', '')
    
    if query:
        categories = Category.objects.filter(name__icontains=query)
    else:
        categories = Category.objects.all()
    
    context = {
        'categories_list' : categories,
        'query' : query,
    }
    return render(request, "categories/categories.html", context)

# Categories list
class CategoriesDashboardView(ListView):
    model = Category
    context_object_name = "categories_list"
    template_name = "categories/categories.html"

    def get_queryset(self):
        return super().get_queryset().annotate(
            total_favorites = Count("recipe__favorites", distinct=True),
            total_recipes = Count("recipe", distinct=True)
        ).order_by("-total_recipes")


