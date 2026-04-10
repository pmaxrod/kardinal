from django.db import models
from django.conf import settings

from wagtail.models import Page
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageBlock
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

class BlogPage(Page):
    # El propietario de la página es el usuario asociado
    content_panels = Page.content_panels + [
        FieldPanel("owner"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("owner")
    ]

    subpage_types = ["PostPage"]

    title = f"Blog de {'owner__username'}"
    slug = "owner__username.lower()"
    
    class Meta:
        verbose_name = "Página de Blog"
 
class PostPage(Page):
    """
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    """
    #content = RichTextField(blank=True)
    # Se migra a StreamField porque da más versatilidad
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", label="Encabezado", required=False)),
        ('paragraph', blocks.RichTextBlock(label="Párrafo", required=False)),
        ('image', ImageBlock(label="Imagen", required=False, search_index=False))
    ], block_counts={
        'image': {'max_num': 10}
    }, default=None)
    tags = ClusterTaggableManager(through="blog.PostPageTag", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    search_fields = Page.search_fields + [
        index.SearchField("tags")
    ]

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("tags"),
    ]

    parent_page_types = ["BlogPage"]
    subpage_types = []

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        get_latest_by = "created_at"

# Etiquetas
@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
 
# Modelo que conecta los posts con las etiquetas
class PostPageTag(TaggedItemBase):
    content_object = ParentalKey("PostPage", related_name="post_tags")