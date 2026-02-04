from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.db.models import Count, Q
from .models import Recipe, Category

#Categories seeker
def search_categories(request):
    query = request.GET.get('q', '')
    
    if query:
        categories = Category.objects.filter(name__icontains=query).annotate(
            total_favorites = Count("recipe__favorites", distinct=True),
            total_recipes = Count("recipe", distinct=True)
        ).order_by("-total_recipes", "-total_favorites")
        
    else:
        categories = Category.objects.all().annotate(
            total_favorites = Count("recipe__favorites", distinct=True),
            total_recipes = Count("recipe", distinct=True)
        ).order_by("-total_recipes", "-total_favorites")
    
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
        ).order_by("-total_recipes", "-total_favorites")

#Recipes seeker
def search_recipes(request):
    query = request.GET.get('q', '')
    
    #Get total recipes
    total_recipes = Recipe.objects.count()

    recipes = Recipe.objects.select_related(
            "category",
            "user",
            "difficulty"
    ).prefetch_related(
        "subcategories",
        "ingredients"
    )

    if query:
        recipes = recipes.filter(
            Q(name__icontains=query) |
            Q(subcategories__name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__name__icontains=query)
        ).distinct()

        recipes = recipes.annotate(
            total_favorites = Count("favorites", distinct=True)
        ).order_by("-total_favorites")
        
    else:
        recipes = Recipe.objects.annotate(
            total_favorites = Count("favorites", distinct=True)
        ).order_by("-total_favorites")
    
    #how much recipes we have after filter
    filtered_recipes = recipes.count()

    context = {
        'recipes_list' : recipes,
        'query' : query,
        'is_filtered': filtered_recipes < total_recipes
    }
    return render(request, "recipes/recipes.html", context)

#Recipes list
class RecipesDashboardView(ListView):
    model = Recipe
    context_object_name = "recipes_list"
    template_name = "recipes/recipes.html"

    def get_queryset(self):
        #Se usa select_relatred para ForeignKeys y se usa prefetch_related para ManyToMany
        return super().get_queryset().select_related(
            "category",
            "user",
            "difficulty"
        ).prefetch_related(
            "subcategories",
        ).annotate(
            total_favorites = Count("favorites", distinct=True)
        ).order_by("-total_favorites")

    