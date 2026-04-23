from django.conf import settings
from django.db import models
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    PublishingPanel,
)
from wagtail.fields import RichTextField
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
)
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)
from wagtail.snippets.models import register_snippet


@register_setting
class NavigationSettings(BaseGenericSetting):
    linkedin_url = models.URLField(verbose_name="URL de Linkedin", blank=True)
    github_url = models.URLField(verbose_name="URL de Github", blank=True)
    mastodon_url = models.URLField(verbose_name="URL de Mastodon", blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("linkedin_url"),
                FieldPanel("github_url"),
                FieldPanel("mastodon_url"),
            ],
            "Configuración de redes sociales",
        )
    ]

    class Meta:
        verbose_name = "Configruación de Navegación"


@register_snippet
class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):

    body = RichTextField()

    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Texto del pie"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Texto del pie"


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    edited_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def edited(self):
        """Comprueba si un objeto ha sido modficado tras su creación.

            Compara sus propiedades created_at y edited_at

        Returns:
            True si created_at no vale lo mismo que edited_at

            False en caso contrario
        """
        return self.edited_at.second != self.created_at.second

    class Meta:
        abstract = True

class CustomImage(AbstractImage):
    caption = models.CharField(max_length=255, blank=True)
    admin_form_fields = Image.admin_form_fields + ('caption',)
    @property
    def default_alt_text(self):
        return getattr(self, "description", None)
    
class CustomRendition(AbstractRendition):
    image = models.ForeignKey(settings.WAGTAILIMAGES_IMAGE_MODEL, on_delete=models.CASCADE, related_name="renditions")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("image", "filter_spec", "focal_point_key"),
                name="unique_rendition"
            )
        ]
    