from django.db import models
from django.conf import settings

from comments.views import create_comment
from base.blocks import CommonContentBlock
from wagtail.models import Page
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, path, re_path
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager


class BlogPage(RoutablePageMixin, Page):
    # El propietario de la página es el usuario asociado
    content_panels = Page.content_panels + [
        FieldPanel("owner"),
    ]

    search_fields = Page.search_fields + [index.SearchField("owner")]

    subpage_types = ["PostPage"]

    title = f"Blog de {'owner__username'}"
    slug = "owner__username.lower()"

    def get_posts(self):
        """Devuelve las entradas del blog

        Returns:
            Array con las entradas del blog
        """
        return PostPage.objects.child_of(self).live()
        # return self.get_children().specific().live()

    @path("")
    def blog_page(self, request):
        """Vista para la página de blog

        Arguments:
            request -- Petición realizada a la aplicación web
        """
        posts = self.get_posts()
        return self.render(request, context_overrides={"posts": posts})

    @re_path(r"^tagged/(?P<tag>[-\w]+)/$")
    def tagged_posts(self, request, tag):
        """Muestra las entradas de un blog etiquetadas con una etiqueta en concreto
        Si la etiqueta tiene espacios, se reemplazan con '-'
        Arguments:
            request -- Petición realizada a la aplicación web
            tag     -- Etiqueta por la que filtrar
        """
        posts = self.get_posts().filter(tags__slug=tag)
        return self.render(request, context_overrides={"posts": posts})

    class Meta:
        verbose_name = "Página de Blog"


class PostPage(RoutablePageMixin, Page):
    body = StreamField(CommonContentBlock())
    tags = ClusterTaggableManager(through="blog.PostPageTag", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    search_fields = Page.search_fields + [index.SearchField("tags")]

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("tags"),
    ]

    parent_page_types = ["BlogPage"]
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["tags"] = self.tags.all()
        context["comments"] = self.comments.all()

        return context

    @path("")
    def post_page(self, request):
        """Vista de la entrada de un blog.
        Se sobreescribe para poder mostrar el formulario de comentarios.

        Arguments:
            request -- Petición realizada a la aplicación web

        """
        form = create_comment(request, self)
        return self.render(request, context_overrides={'form': form})

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
