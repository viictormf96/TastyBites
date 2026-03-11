from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from .models import Recipe, Category


#Funcion para filtrar recetas
def recipes_serch_filter(query_set, search_query):
    query_set = query_set.filter(
        Q(name__icontains=search_query) |
        Q(subcategories__name__icontains=search_query) |
        Q(user__username__icontains=search_query) |
        Q(user__first_name__icontains=search_query) |
        Q(user__last_name__icontains=search_query) |
        Q(category__name__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(ingredients__name__icontains=search_query)
    ).distinct()

    return query_set

def recipes_filters(queryset, params):
        # 4. Mapeo de Filtros
        time_map = {
            "15": {"cooking_time__lt": 15},
            "15_30": {"cooking_time__range": (15, 30)},
            "30_60": {"cooking_time__range": (30, 60)},
            "60": {"cooking_time__gt": 60},
        }
        
        diff_map = {
            "easy": 1, 
            "medium": 2, 
            "difficult": 3
        }

        calories_map = {
            "300": {"calories__lt": 300},
            "300_600": {"calories__range": (300, 600)},
            "600_900": {"calories__range": (600, 900)},
            "900": {"calories__gt": 900},
        }

        diet_map = {
            "vegan": "vegano",
            "keto": "keto",
            "gluten_free": "Sin gluten",
            "lactos_free": "Sin lactosa",
        }

        # 5. Aplicación dinámica de filtros
        if (t := params.get('time')) in time_map:
            queryset = queryset.filter(**time_map[t])
            
        if (d := params.get('difficulty')) in diff_map:
            queryset = queryset.filter(difficulty=diff_map[d])
            
        if (c := params.get('calories')) in calories_map:
            queryset = queryset.filter(**calories_map[c])
            
        if (diet := params.get('diet')) in diet_map:
            queryset = queryset.filter(subcategories__name__iexact=diet_map[diet])
        
        return queryset

def featured_recipe(recipes):
    now = timezone.now()
    last_moth = now - timedelta(days=30)

    recipe = recipes.annotate(
        total_fav_lastmoth = Count(
            'favorites',
            filter=Q(favorites__created_at__gte=last_moth),
            distinct=True
        )
    ).order_by("-total_fav_lastmoth", "-total_favorites").first()

    if recipe and getattr(recipe, 'total_fav_lastmonth', 0) > 0:
        return recipe
    
    return recipes.order_by("-total_favorites").first()

# Category view
class CategoryDashboardView(ListView):
    model = Recipe
    context_object_name = "recipes_list"
    template_name = "category/category.html"
    
    def get_queryset(self):

        self.category = get_object_or_404(Category, slug=self.kwargs['slug_category'])

        category_recipes = Recipe.objects.filter(category = self.category).select_related(
            "user", "difficulty"
        ).prefetch_related(
            "subcategories"
        ).annotate(
            total_favorites=Count("favorites", distinct=True)
        )

        #Total favoritos
        self.total_fav = category_recipes.aggregate(
            total_general = Sum("total_favorites")
        ) 

        self.total_recipes = category_recipes

        #Obtenemos datos del formulario
        params = self.request.GET
        search_query = params.get('q', '')
        subcategory_filter = params.get('sub', '')

        # Filters
        if search_query:
            category_recipes = recipes_serch_filter(category_recipes, search_query)

        if params.get('time') or params.get('difficulty') or params.get('calories'):
            category_recipes = recipes_filters(category_recipes, params) 

        if subcategory_filter:
            category_recipes = category_recipes.filter(subcategories__slug__exact=subcategory_filter)

        #Ordenación
        sort_by = params.get('sort', 'popular')
        ordering = "-total_favorites" if sort_by == "popular" else "-created_at"
        
        return category_recipes.order_by(ordering)

    #Paginate recipes
    def get_paginate_by(self, queryset):
        view_mode = self.request.GET.get('view', 'grid')
        if view_mode == 'list':
            return 4  # Modo lista: 4 elementos
        return 6  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Lista de subcategorias(category es el related_name puesto en subcategory)
        subcategories_list =self.category.category.all()
        actual_recipes = context['recipes_list']
        filtred_count = actual_recipes.count()
        total_recipes = self.total_recipes.count()
        recipe_fav_lastmoth = featured_recipe(self.total_recipes)

        context.update({
            "category" : self.category,
            "actual_recipes": actual_recipes,
            "recipes_totals" : total_recipes,
            "recipes_fav_total" : self.total_fav["total_general"] or 0,
            "featured_recipe" : recipe_fav_lastmoth,
            "subcategories" : subcategories_list,
            "query" :  self.request.GET.get('q', ''),
            "is_filtred": filtred_count < total_recipes,
            "view_mode": self.request.GET.get('view', 'grid'),
            "time_filter": self.request.GET.get('time'),
            "difficulty_filter": self.request.GET.get('difficulty'),
            "calories_filter": self.request.GET.get('calories'),
            "current_sub": self.request.GET.get('sub'),
        })

        return context

# Categories view
class CategoriesDashboardView(ListView):
    model = Category
    context_object_name = "categories_list"
    template_name = "categories/categories.html"

    def get_queryset(self):

        queryset = super().get_queryset()

        search_query = self.request.GET.get('q')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)|
                Q(description__icontains=search_query)
            ).distinct()
        
        queryset = queryset.annotate(
            total_favorites = Count("recipes__favorites", distinct=True),
            total_recipes = Count("recipes", distinct=True)
        ).order_by("-total_recipes", "-total_favorites")

        return queryset
    
    #Paginate Categories
    def get_paginate_by(self, queryset):
        view_mode = self.request.GET.get('view', 'grid')
        if view_mode == 'list':
            return 4  
        return 8  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        full_queryset = self.get_queryset()
        total_categories = Category.objects.count()
        actual_categories = context['categories_list']
        filtred_count = actual_categories.count()

        context.update({
            "query" : self.request.GET.get('q', ''),
            "actual_categories": actual_categories,
            "filtred_count": filtred_count,
            "view_mode": self.request.GET.get('view', 'grid'),
            "total_categories": full_queryset.count(),
            "is_filtred": total_categories > filtred_count,
        })

        return context

#Recipes view
class RecipesDashboardView(ListView):
    model = Recipe
    context_object_name = "recipes_list"
    template_name = "recipes/recipes.html"

    def get_queryset(self):
        # 1. Base optimizada con relaciones
        queryset = super().get_queryset().select_related(
            "category", "user", "difficulty"
        ).prefetch_related("subcategories")

        # 2. Captura de parámetros
        params = self.request.GET
        search_query = params.get('q')
        
        # 3. Búsqueda Global (Q Objects)
        if search_query:
            queryset = recipes_serch_filter(queryset, search_query)

        if params.get('time') or params.get('difficulty') or params.get('calories') or params.get('diet'):
            queryset = recipes_filters(queryset, params) 
        
        # 6. Anotación y Ordenación
        queryset = queryset.annotate(total_favorites=Count("favorites", distinct=True))
        
        sort_by = params.get('sort', 'popular')
        ordering = "-total_favorites" if sort_by == "popular" else "-created_at"
    
        return queryset.order_by(ordering)

    #Paginate recipes
    def get_paginate_by(self, queryset):
        view_mode = self.request.GET.get('view', 'grid')
        if view_mode == 'list':
            return 4  # Modo lista: 4 elementos
        return 6  

    def get_context_data(self, **kwargs):
        #We send extra info to template
        context = super().get_context_data(**kwargs)

        full_queryset = self.get_queryset()
        total_recipes = Recipe.objects.count()
        actual_recipes = context['recipes_list']
        filtred_count = actual_recipes.count()

        context.update({
            "query" : self.request.GET.get('q', ''),
            "is_filtred": filtred_count < total_recipes,
            "actual_recipes": actual_recipes,
            "total_recipes": full_queryset.count(),
            "view_mode": self.request.GET.get('view', 'grid'),
            "time_filter": self.request.GET.get('time'),
            "difficulty_filter": self.request.GET.get('difficulty'),
            "calories_filter": self.request.GET.get('calories'),
            "diet_filter": self.request.GET.get('diet'),
        })
        
        return context

#Recipe view

class RecipeDashboardView(DetailView):
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipe/recipe.html"

    slug_field = "slug"
    slug_url_kwarg= "slug_recipe"
    
    def get_queryset(self):
        
        return Recipe.objects.prefetch_related("instruction", "ingredients")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        context["instructions"] = recipe.instruction.all()
        context["ingredients"] = recipe.ingredients.all()
        return context
    