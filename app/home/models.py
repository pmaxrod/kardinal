from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from base.models import BasePage
from home.blocks import HomeContentBlock


class HomePage(BasePage):
    body = StreamField(
        HomeContentBlock(),
        blank=True,
        use_json_field=True,
        verbose_name=_("Contenido"),
        help_text=_("Contenido de la página de inicio",)
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("body"),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["dashboard.DashboardPage"]

    class Meta:
        verbose_name = _("Página de Inicio")
        verbose_name_plural = _("Páginas de Inicio")
