from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Count
from .models import Recipe, Category

#BASE CLASS
class RecipeListBaseView(ListView):
    #List and paginator functionality. All the views inheritance form this one to reuse the config.
    model = Recipe
    context_object_name = "recipes" #Object name in the template
    paginate_by = 10

#INDEX / MAIN CLASS (URL: /)
class IndexDashboardView(RecipeListBaseView):
    template_name = "recipes/recipe_list_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #highlighted recipies (3 random)
        context["featured_recipes"] = Recipe.objects.all().order_by("?")[:3]

        #Categories with Recipies count
        """  context["categories"] = Category.objects.annotate(
            recipe_count = Count("recipes")
        ).order_by(
            "-recipe_count",
            "name"
        )

        """
        return context
