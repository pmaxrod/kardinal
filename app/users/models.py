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


class AppSettings(models.Model):
    # Se crean tipos enumerados para la configuración de usuario
    class AppTheme(models.TextChoices):
        DEFAULT = "default", _("Tema del navegador")
        LIGHT = "light", _("Tema claro")
        DARK = "dark", _("Tema oscuro")

    class AppFontFamily(models.TextChoices):
        SANS_SERIF = "font-sans-serif", _("Fuente sans-serif")
        SERIF = "font-serif", _("Fuente serif")

    # El usuario puede ser nulo porque los usuarios sin sesión
    # pueden cambiar preferencias aun si no se guardan
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        blank=True,
        null=True,
        default=None,
    )
    theme = models.CharField(
        choices=AppTheme,
        default=AppTheme.DEFAULT,
        verbose_name=_("Tema"),
        help_text=_("Tema de la aplicación"),
    )
    font = models.CharField(
        choices=AppFontFamily,
        default=AppFontFamily.SANS_SERIF,
        verbose_name=_("Fuente"),
        help_text=_("Tipo de fuente para la aplicación"),
    )

    class Meta:
        verbose_name = _("Configuración de usuario")
        verbose_name_plural = _("Configuraciones de usuario")
