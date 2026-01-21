from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.db.models import Count
from recipes.models import Recipe, Category

User = get_user_model()

#INDEX / MAIN CLASS (URL: /)
class IndexDashboardView(TemplateView):
    template_name = "index/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #highlighted recipies (3 random)
        context["featured_recipes"] = Recipe.objects.annotate(
            likes_count=Count("favorites", distinct=True),
            comments_count=Count("comments", distinct=True) 
        ).order_by("-likes_count", "-comments_count")[:3]

        #Categories with Recipies count
        context["categories"] = Category.objects.annotate(
            recipe_count = Count("recipe")
        ).order_by(
            "-recipe_count",
            "name"
        )[:4]

        return context

# ABOUT CLASS (URL: about/)
class AboutView(TemplateView):
    template_name = "about/about.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["top_chefs"] = User.objects.annotate(
            recipe_count=Count('recipe')
        ).order_by('-recipe_count')[:3]
        
        return context

