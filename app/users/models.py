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

    class Meta:
        get_latest_by = "date_joined"
        ordering = ["username"]