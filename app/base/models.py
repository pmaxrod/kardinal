from django import forms
from django.conf import settings
from django.db import models
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    PublishingPanel,
    TabbedInterface,
)
from wagtail.fields import RichTextField
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
    Page,
)
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)
from wagtail.documents.models import AbstractDocument, Document
from wagtail.snippets.models import register_snippet
from wagtail.search import index


# Páginas de configuración
@register_setting
class NavigationSettings(BaseGenericSetting):
    """Configuración global de enlaces relacionados con el sitio web.

    Attributes:

    """

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


# Snippets
@register_snippet
class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):
    """Snippet para el texto del pie del sitio web.

    Arguments:
        body -- Contenido del texto del pie
    """

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


# Mixins
class TimeStampedMixin(models.Model):
    """Mixin para modelos de los que se quiere registrar su fecha de creación y modificación.

    Attributes:
        created_at -- Fecha de creación del registro
        updated_at -- Fecha de modificación del registro

    Methods:
        edited(self) -- Comprueba si el registro ha sido editado o no
    """

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    edited_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def edited(self):
        """Comprueba si un objeto ha sido modficado tras su creación.

        Returns:
            True si created_at no vale lo mismo que edited_at

            False en caso contrario
        """
        return self.edited_at.second != self.created_at.second

    class Meta:
        abstract = True


class Like(models.Model):
    """Modelo base para los 'Me gusta' de la aplicación."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes"
    )
    liked_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Me Gusta")

    class Meta:
        abstract = True


# Modelos personalizados
class BasePage(Page):
    """Modelo abstracto base para las páginas.

    Se le añade un campo de descripción a la página y un array
    de paneles laterales en caso de ser necesarios.
    """

    description = models.CharField(
        blank=True, verbose_name="Descripción", help_text="Descripción de la página"
    )

    # Definición para las páginas que lo necesiten
    sidebar_panels = []
    content_panels = Page.content_panels + [FieldPanel("description")]
    promote_panels = Page.promote_panels
    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("first_published_at", read_only=True),
                FieldPanel("last_published_at", read_only=True),
            ],
            heading="Fechas de publicación",
            icon="date",
            classname="collapsed",
        ),
        FieldPanel("owner", read_only=True, icon="user", permission="superuser"),
        FieldPanel("live", read_only=True, icon="view", permission="superuser"),
    ]

    search_fields = Page.search_fields + [index.FilterField("description")]
    edit_handlers = TabbedInterface(
        [
            ObjectList(content_panels, heading="Contenido"),
            ObjectList(sidebar_panels, heading="Barra lateral"),
            ObjectList(settings_panels, heading="Configuración"),
            ObjectList(promote_panels, heading="Promocionar", permission="superuser"),
        ]
    )

    class Meta:
        abstract = True


class CustomImage(AbstractImage):
    """Modelo de imagen de Wagtail personalizado.

    Attributes:
        caption -- Leyenda de la imagen
    """

    caption = models.CharField(max_length=255, blank=True, verbose_name="Leyenda")

    admin_form_fields = Image.admin_form_fields + ("caption",)

    @property
    def default_alt_text(self):
        return getattr(self, "description", None)


class CustomRendition(AbstractRendition):
    """Modelo de rendición de imagen de Wagtail personalizado.

    Attributes:
        image -- Referencia a la imagen renderizada.
    """

    image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        on_delete=models.CASCADE,
        related_name="renditions",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("image", "filter_spec", "focal_point_key"),
                name="unique_rendition",
            )
        ]


class CustomDocument(AbstractDocument):
    """Modelo de documento personalizado de Wagtail.

    Attributes:
        source -- Fuente del documento
    """

    source = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Fuente"
    )

    admin_form_fields = Document.admin_form_fields + ("source",)
