from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
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
from wagtail.documents.models import AbstractDocument, Document
from wagtail.search import index


# Modelos
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

    body = RichTextField(
        verbose_name=_("Contenido"), help_text=_("Contenido del texto del pie")
    )

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
        verbose_name = _("Texto del pie")
        verbose_name_plural = _("Textos del pie")


class SocialMediaLink(DraftStateMixin, RevisionMixin, models.Model):
    """Snippet para enlaces de redes sociales.

    Arguments:
        url -- URL de la cuenta
        name -- Nombre de la red social
    """

    url = models.URLField(
        blank=False,
        null=False,
        verbose_name=_("URL"),
        help_text=_("URL de la cuenta de la red social"),
        max_length=200,
    )
    name = models.CharField(
        blank=False,
        null=False,
        verbose_name=_("Nombre"),
        help_text=_("Nombre de la red social"),
    )

    panels = [
        FieldPanel("url"),
        FieldPanel("name"),
        PublishingPanel(),
    ]

    def __str__(self):
        return f"Enlace a {self.name}"

    class Meta:
        verbose_name = _("Enlace de redes sociales")
        verbose_name_plural = _("Enlaces de redes sociales")


class AppThemes(models.TextChoices):
    """Temas de la aplicación."""
    DEFAULT = "", _("Navegador")
    LIGHT = "light", _("Claro")
    DARK = "dark", _("Oscuro")


class AppFontFamilies(models.TextChoices):
    """Tipos de fuente de la aplicación."""

    SANS_SERIF = "font-sans-serif", _("Fuente sans-serif")
    SERIF = "font-serif", _("Fuente serif")


class TimeStampedMixin(models.Model):
    """Mixin para modelos de los que se quiere registrar su fecha de creación y modificación.

    Attributes:
        created_at -- Fecha de creación del registro
        updated_at -- Fecha de modificación del registro

    Methods:
        edited(self) -- Comprueba si el registro ha sido editado o no
    """

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha de creación")
    )
    edited_at = models.DateTimeField(auto_now=True, verbose_name=_("Fecha de edición"))

    @property
    def edited(self):
        """Comprueba si un objeto ha sido modficado tras su creación.

        Returns:
            True si created_at no vale lo mismo que edited_at

            False en caso contrario
        """
        return self.created_at != self.edited_at

    class Meta:
        abstract = True


class Like(models.Model):
    """Modelo base para los 'Me gusta' de la aplicación."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha de Me Gusta")
    )

    class Meta:
        abstract = True


# Modelos personalizados de Wagtail
class BasePage(Page):
    """Modelo abstracto base para las páginas.

    Se le añade un campo de descripción a la página y un array
    de paneles laterales en caso de ser necesarios.
    """

    subtitle = models.CharField(
        blank=True, verbose_name=_("Subtítulo"), help_text=_("Subtítulo de la página")
    )

    # Definición para las páginas que lo necesiten
    sidebar_panels = []
    content_panels = Page.content_panels + [FieldPanel("subtitle")]
    promote_panels = Page.promote_panels
    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("first_published_at", read_only=True),
                FieldPanel("last_published_at", read_only=True),
            ],
            heading=_("Fechas de publicación"),
            icon="date",
            classname="collapsed",
        ),
        FieldPanel("owner", read_only=True, icon="user", permission="superuser"),
        FieldPanel("live", read_only=True, icon="view", permission="superuser"),
    ]

    search_fields = Page.search_fields + [index.FilterField("subtitle")]
    edit_handlers = TabbedInterface(
        [
            ObjectList(content_panels, heading=_("Contenido")),
            ObjectList(sidebar_panels, heading=_("Barra lateral")),
            ObjectList(
                promote_panels, heading=_("Promocionar"), permission="superuser"
            ),
            ObjectList(settings_panels, heading=_("Configuración")),
        ]
    )

    @property
    def edited(self):
        return not self.first_published_at == self.last_published_at

    class Meta:
        abstract = True


class CustomImage(AbstractImage):
    """Modelo de imagen de Wagtail personalizado.

    Attributes:
        caption -- Leyenda de la imagen
    """

    caption = models.CharField(max_length=255, blank=True, verbose_name=_("Leyenda"))

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
        max_length=255, blank=True, null=True, verbose_name=_("Fuente")
    )

    admin_form_fields = Document.admin_form_fields + ("source",)
