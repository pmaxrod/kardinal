from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """Modelo de usuario personalizado."""

    bio = models.TextField(
        max_length=200,
        blank=True,
        default="",
        verbose_name=_("Biografía"),
        help_text=_("Escribe sobre tí"),
    )
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        verbose_name=_("Seguidores"),
        symmetrical=False,
    )

    @property
    def follower_count(self):
        """Devuelve el número de seguidores del usuario."""
        return self.followed_by.count()

    @property
    def following_count(self):
        """Devuelve el número de usuarios seguidos."""
        return self.follows.count()

    def follow(self, user):
        """Sigue a un usuario."""
        self.follows.add(user)

    def unfollow(self, user):
        """Deja de seguir a un usuario."""
        self.follows.remove(user)

    def is_following(self, user):
        """Comprueba si un usuario sigue a otro."""
        return self.follows.filter(pk=user.pk).exists()

    def __str__(self):
        return self.username

    class Meta:
        get_latest_by = "date_joined"
        ordering = ["username"]
