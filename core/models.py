from django.db import models
from recipes.models import Recipe
from accounts.models import CustomUser

# Recipe Comments model
class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recipe = models.ForeignKey(Recipe, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        db_table = "comments"
    
    def __str__(self):
        return f"Comentario de {self.user.username} en {self.recipe.name}"

# Favorite Recipes model
class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name="favorites", on_delete=models.CASCADE)
    class Meta:
        db_table = "favorites"
        unique_together = ("user", "recipe")
    def __str__(self):
        return f"{self.user.username} le gusta {self.recipe.name}"

    

