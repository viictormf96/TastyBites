from django.contrib.auth.models import AbstractUser
from django.db import models

# User model
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(default="null", upload_to="accounts/avatars/")

    class Meta:
        db_table = "users"

# Followers model
class Follower(models.Model):
    follower = models.ForeignKey(CustomUser, related_name="following", on_delete=models.CASCADE)
    followee = models.ForeignKey(CustomUser, related_name="followers", on_delete=models.CASCADE)
    class Meta:
        db_table = "followers"
        unique_together = ("follower", "followee")
    def __str__(self):
        return f"{self.follower.username} sigue {self.followee.username}"

