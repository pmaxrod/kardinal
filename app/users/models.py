from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from wagtail.users.models import upload_avatar_to



# Create your models here.
class User(AbstractUser):
    bio = models.TextField(
        max_length=200,
        blank=True,
        default="",
        verbose_name=_("Biografía"),
        help_text=_("Escribe sobre tí"),
    )
    profile_picture = models.ImageField(
        upload_to=upload_avatar_to,
        null=True,
        blank=True,
        verbose_name=_("Foto de perfil"),
        help_text=_("Foto de perfil de la cuenta"),
    )

    @property
    def has_pfp(self):
        """Comprueba si el usuario tiene una foto de perfil

        Returns:
            True si la tiene; False en caso contrario
        """
        return self.profile_picture.url != None

    class Meta:
        get_latest_by = "date_joined"
        ordering = ["username"]