from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField

# import MultiFieldPanel:
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

class HomePage(Page):
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Imagen de inicio",
    )

    hero_text = models.CharField(
        blank=True,
        max_length=255, help_text="Introducción del sitio"
    )

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("hero_text")
            ],
            heading="Sección",
        ),
        FieldPanel('body'),
    ]
    
    subpage_types = ["blog.BlogPage"]
    
    class Meta:
        verbose_name = "Página de Inicio"
