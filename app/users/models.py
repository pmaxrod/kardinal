from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(
        max_length=200, help_text="Escribe sobre tí", verbose_name="Biografía"
    )
    profile_picture = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        help_text="Foto de perfil de la cuenta",
        verbose_name="Foto de perfil",
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
        


class UserAppSettings(models.Model):
    # Se crean tipos enumerados para la configuración de usuario
    class AppTheme(models.TextChoices):
        SYSTEM = "system", "Tema predeterminado del sistema"
        LIGHT = "light", "Tema claro"
        DARK = "dark", "Tema oscuro"

    class AppFontFamily(models.TextChoices):
        SANS_SERIF = "font-sans-serif", "Fuente sans-serif"
        SERIF = "font-serif", "Fuente serif"

    # El usuario puede ser nulo porque los usuarios sin sesión
    # pueden cambiar preferencias aun si no se guardan
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="settings",
        blank=True,
        null=True,
        default=None,
    )
    theme = models.CharField(
        choices=AppTheme,
        default=AppTheme.SYSTEM,
        verbose_name="Tema",
        help_text="Tema de la aplicación",
    )
    font = models.CharField(
        choices=AppFontFamily,
        default=AppFontFamily.SANS_SERIF,
        verbose_name="Fuente",
        help_text="Tipo de fuente para la aplicación",
    )

    class Meta:
        verbose_name = "settings"
