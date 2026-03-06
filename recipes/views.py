from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.db.models import Count, Q, Sum
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


class CategoryDashboardView(DetailView):
    model = Category
    context_object_name = "category"
    template_name = "category/category.html"
    
    # Especificamos cómo encontrar la categoría en la URL
    slug_url_kwarg = 'slug_category'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        #Recipes List
        recipes_list = self.object.recipes.select_related(
            "user", "difficulty"
        ).prefetch_related(
            "subcategories"
        ).annotate(
            total_favorites = Count("favorites", distinct=True)
        ).order_by(
            "-total_favorites"
        )

        #Obtenemos datos del formulario
        params = self.request.GET
        search_query = params.get('q', '')
        subcategory_filter = params.get('sub', '')

        # Filters
        if search_query:
            recipes_list = recipes_serch_filter(recipes_list, search_query)

        if params.get('time') or params.get('difficulty') or params.get('calories'):
            recipes_list = recipes_filters(recipes_list, params) 

        if subcategory_filter:
            recipes_list = recipes_list.filter(subcategories__slug__exact=subcategory_filter)

        #Lista de subcategorias
        subcategories_list = self.object.category.all()

        #Anotación
        recipes_list = recipes_list.annotate(total_favorites=Count("favorites", distinct=True))

        #Count del total de likes de todas las recetas de la categoria.
        totals= recipes_list.aggregate(
            total_general = Sum("total_favorites")
        )        
        
        #Ordenación
        sort_by = params.get('sort', 'popular')
        ordering = "-total_favorites" if sort_by == "recent" else "-created_at"
        recipes_list = recipes_list.order_by(ordering)

        context.update({
            "recipes_list" : recipes_list,
            "recipes_fav_total" : totals["total_general"] or 0,
            "subcategories" : subcategories_list,
            "query" : search_query,
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
            total_favorites = Count("recipe__favorites", distinct=True),
            total_recipes = Count("recipe", distinct=True)
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
        ordering = "-total_favorites" if sort_by == "recent" else "-created_at"
    
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
    

