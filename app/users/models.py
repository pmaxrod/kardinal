from django.db import models
from django.conf import settings

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=750, verbose_name="Biografía")
    profile_picture = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Foto de perfil",
        verbose_name="Foto de perfil",
    )

    def __iter__(self):
        fields = self._meta.get_fields()
        for field in fields:
            yield (field.name)

    class Meta:
        verbose_name = "profile"
        get_latest_by = "date_joined"
        ordering = ["user__username"]