from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()

# ABOUT CLASS (URL: about/)

class AboutView(TemplateView):
    template_name = "about/about.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["top_chefs"] = User.objects.annotate(
            recipe_count=Count('recipe')
        ).order_by('-recipe_count')[:3]
        
        return context

