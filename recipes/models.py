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
    
# Recipe model 
class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    cooking_time = models.IntegerField()
    image = models.ImageField(upload_to="recipes/")
    difficulty = models.CharField(max_length=50)
    followers = models.IntegerField(default=0)
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
    
# Recipe Comments model
class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "comments"
    
    def __str__(self):
        return f"Comentario de {self.user.username} en {self.recipe.name}"

# Favorite Recipes model
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    class Meta:
        db_table = "favorites"
        unique_together = ("user", "recipe")
    def __str__(self):
        return f"{self.user.username} le gusta {self.recipe.name}"

# Followers model
class Follower(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    class Meta:
        db_table = "followers"
        unique_together = ("follower", "followee")
    def __str__(self):
        return f"{self.follower.username} sigue {self.followee.username}"
    

