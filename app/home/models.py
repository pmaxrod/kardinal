from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from base.models import BasePage
from home.blocks import HomeContentBlock


class HomePage(BasePage):
    body = StreamField(
        HomeContentBlock(),
        blank=True,
        use_json_field=True,
        help_text="Cuerpo de la página de inicio",
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Página de Inicio"
