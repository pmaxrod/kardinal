from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class CustomUser(AbstractUser):
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(unique=True, max_length=25)
    bio = models.TextField(max_length=750)
    profile_picture = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Foto de perfil",
    )
    
    class Meta:
        verbose_name = "profile"
        get_latest_by = "date_joined"
        ordering = ["username"]
        indexes = [models.Index(fields=["username"], name="username_index")]