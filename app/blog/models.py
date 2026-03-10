from django.db import models
from django.conf import settings

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from taggit.models import Tag as TaggitTag, TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

class BlogPage(Page):
    pass
    class Meta:
        verbose_name = "Página de Blog"
 
class PostPage(Page):
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content = RichTextField(blank=True)
    tags = ClusterTaggableManager(through="blog.PostPageTag", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="user")

    content_panels = Page.content_panels + [
        FieldPanel("header_image"),
        # InlinePanel("categories", label="categoría"),
        FieldPanel("content"),
        FieldPanel("tags"),
    ]
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        get_latest_by = "created_at"
        #indexes = [models.Index(fields=["tags"], name="tags_index")]

# Etiquetas
@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"

""" @register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)
 
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]
    def __str__(self):
        return self.name
 
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
 """ 
 
# Modelo que conecta los posts con las etiquetas
class PostPageTag(TaggedItemBase):
    content_object = ParentalKey("PostPage", related_name="post_tags")
""" class PostPageBlogCategory(models.Model):
    page = ParentalKey(
        "blog.PostPage", on_delete=models.CASCADE, related_name="categories"
    )
    blog_category = models.ForeignKey(
        "blog.BlogCategory", on_delete=models.CASCADE, related_name="post_pages"
    )
 
    panels = [
        FieldPanel("blog_category"),
    ]
 
    class Meta:
        unique_together = ("page", "blog_category")
 """ 
 
