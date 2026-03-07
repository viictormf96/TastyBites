from django.db import models
from accounts.models import CustomUser as User
from django.utils.text import slugify

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name="url")
    image = models.ImageField(upload_to="categories/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "categories"
    
    def save(self, *args, **kwargs):
        # Si el slug no existe (es nuevo o se borró), lo generamos
        if not self.slug:
            self.slug = slugify(self.titulo)
        
        # Llamamos al método save original para que guarde todo en la DB
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    

# Subcategory model
class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name="url")
    category = models.ManyToManyField(Category, related_name="category")

    class Meta:
        db_table = "subcategories"
    
    def save(self, *args, **kwargs):
        # Si el slug no existe (es nuevo o se borró), lo generamos
        if not self.slug:
            self.slug = slugify(self.titulo)
        
        # Llamamos al método save original para que guarde todo en la DB
        super().save(*args, **kwargs)  
    
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
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name="url")
    image = models.ImageField(upload_to="recipes/")
    difficulty = models.ForeignKey(Difficulty, on_delete=models.SET_NULL, null=True)
    servings = models.IntegerField(blank=True, null=True)
    calories = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipes")
    subcategories = models.ManyToManyField(Subcategory)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recipes"
    
    def save(self, *args, **kwargs):
        # Si el slug no existe (es nuevo o se borró), lo generamos
        if not self.slug:
            self.slug = slugify(self.titulo)
        
        # Llamamos al método save original para que guarde todo en la DB
        super().save(*args, **kwargs)   

        # Aseguramos que la subcategoria este en la categoria. 
        if self.subcategories and self.category:    
            # .add() es inteligente: si ya existe la relación, no hace nada.
            # Si no existe, crea el vínculo en la tabla intermedia automáticamente.
            self.subcategories.category.add(self.category)

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
    recipe = models.ForeignKey(Recipe, related_name="ingredients", on_delete=models.CASCADE)
    class Meta:
        db_table = "ingredients"
    
    def __str__(self):
        return f"{self.quantity} de {self.name}"
    