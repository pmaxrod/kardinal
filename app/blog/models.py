from django.db import models

from base.models import TimeStampedModel
from base.blocks import CommonContentBlock
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtail.models import ClusterableModel, Page
from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, path, re_path
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from comments.forms import CommentForm

class BlogIndexPage(RoutablePageMixin, Page):
    # El propietario de la página es el usuario asociado
    content_panels = Page.content_panels + [
        FieldPanel("owner"),
    ]

    search_fields = Page.search_fields + [index.SearchField("owner")]

    # def get_posts(self):
    #     """Devuelve las entradas del blog

    #     Returns:
    #         Array con las entradas del blog
    #     """
    #     return BlogPost.objects.child_of(self).live()

    # @path("")
    # def blog_page(self, request):
    #     """Vista para la página de blog

    #     Arguments:
    #         request -- Petición realizada a la aplicación web
    #     """
    #     posts = self.get_posts()
    #     return self.render(request, context_overrides={"posts": posts})

    # @re_path(r"^tagged/(?P<tag>[-\w]+)/$")
    # def tagged_posts(self, request, tag):
    #     """Muestra las entradas de un blog etiquetadas con una etiqueta en concreto
    #     Si la etiqueta tiene espacios, se reemplazan con '-'
    #     Arguments:
    #         request -- Petición realizada a la aplicación web
    #         tag     -- Etiqueta por la que filtrar
    #     """
    #     posts = self.get_posts().filter(tags__slug=tag)
    #     return self.render(request, context_overrides={"posts": posts})

    class Meta:
        verbose_name = "Página de Blog"


class BlogPost(TimeStampedModel, ClusterableModel):
    body = StreamField(CommonContentBlock())
    #tags = ClusterTaggableManager(through="blog.BlogPostTag", blank=True)
        
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
class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey("BlogPost", related_name="post_tags")
