from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=25)
    password = models.CharField(max_length=16)
    email = models.EmailField(null=False)
    bio = models.TextField(max_length=750)
    profile_picture = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Foto de perfil",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    blog_page = models.ForeignKey("blog.BlogPage", on_delete=models.CASCADE, related_name="blog_page")
    
    class Meta:
        get_latest_by = "created_at"
        order_by = "username"
        index = models.Index(fields=["username"], name="username_index")
        constraints = [
            models.UniqueConstraint("username", "blog_page", name="unique_username_blog_page")
        ]