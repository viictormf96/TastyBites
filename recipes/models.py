from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os
from django.db import models
from accounts.models import CustomUser as User

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to="categories/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "categories"
    
    def __str__(self):
        return self.name
    

# Subcategory model
class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 

    class Meta:
        db_table = "subcategories"
    
    def __str__(self):
        return self.name

# Difficulty model
class Difficulty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Recipe model 
class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    cooking_time = models.IntegerField()
    image = models.ImageField(upload_to="recipes/")
    difficulty = models.ForeignKey(Difficulty, on_delete=models.SET_NULL, null=True)
    servings = models.IntegerField(blank=True, null=True)
    calories = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategories = models.ManyToManyField(Subcategory)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recipes"
    
    def __str__(self):
        return self.name

# Recipe Instructions model
class Instruction(models.Model):
    step_number = models.IntegerField()
    description = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('recipe', 'step_number')
        db_table = "instructions"
    
    def __str__(self):
        return f"Paso {self.step_number} para {self.recipe.name}"

# Recipe Ingredients model
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    class Meta:
        db_table = "ingredients"
    
    def __str__(self):
        return f"{self.quantity} de {self.name}"
    

@receiver(post_delete, sender=Recipe)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Borra el archivo del sistema cuando se elimina el objeto de la base de datos.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=Recipe)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Borra el archivo antiguo cuando se sube uno nuevo.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)