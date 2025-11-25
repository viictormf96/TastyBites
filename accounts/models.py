from django.contrib.auth.models import AbstractUser
from django.db import models

# User model

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(default="null", upload_to="accounts/avatars/")

    class Meta:
        db_table = "users"



