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


#Recipes view
class RecipesDashboardView(ListView):
    model = Recipe
    context_object_name = "recipes_list"
    template_name = "recipes/recipes.html"

    def get_queryset(self):

         #Se usa select_relatred para ForeignKeys y se usa prefetch_related para ManyToMany
        queryset = super().get_queryset().select_related(
            "category",
            "user",
            "difficulty"
        ).prefetch_related(
            "subcategories",
        )

        #Recipes seeker
        search_query = self.request.GET.get('q')

        #Recipes filters
        sort_by = self.request.GET.get('sort', 'popular')


        if search_query:
            queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(subcategories__name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(ingredients__name__icontains=search_query)
            ) .distinct()
        
        queryset = queryset.annotate(
            total_favorites = Count("favorites", distinct=True)
        )
        
        if sort_by == "recent":
            queryset = queryset.order_by("-total_favorites")
        else:   
            queryset = queryset.order_by("-created_at") 

        return queryset

    #Paginate recipes
    def get_paginate_by(self, queryset):
        view_mode = self.request.GET.get('view', 'grid')
        if view_mode == 'list':
            return 4  # Modo lista: 4 elementos
        return 6  

    def get_context_data(self, **kwargs):
        #We send extra info to template
        context = super().get_context_data(**kwargs)

        total_recipes = Recipe.objects.count()
        actual_recipes = context['recipes_list']
        filtred_count = actual_recipes.count()

        context.update({
            "query" : self.request.GET.get('q', ''),
            "is_filtred": filtred_count < total_recipes,
            "actual_recipes": actual_recipes,
            "view_mode": self.request.GET.get('view', 'grid'),
        })
        
        return context
    

