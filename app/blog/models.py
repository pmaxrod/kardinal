import datetime
from django.utils.translation import gettext as _
from django.db import models
from django.conf import settings
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtail.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, path, re_path
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from base.models import BasePage
from blog.blocks import BlogPostBlock
from comments.forms import CommentForm
from comments.models import Comment


class BlogDashboardPage(BasePage):
    """Página que contiene las bandejas de entradas."""

    page_description = _("Página padre de todos los blogs")

    parent_page_types = ["home.HomePage"]
    subpage_types = ["BlogIndexPage"]
    max_count_per_parent = 1

    class Meta:
        verbose_name = _("Página de listado de blogs")
        verbose_name_plural = _("Páginas de listado de blogs")


class BlogIndexPage(RoutablePageMixin, BasePage):
    """Página para el blog de un usuario"""

    class BlogTheme(models.TextChoices):
        DEFAULT = "default", _("Predeterminado")
        KARDINAL = "kardinal", _("Cardenal rojo")

    page_description = _("Blog para un creador de contenido")
    theme = models.CharField(
        choices=BlogTheme,
        default=BlogTheme.DEFAULT,
        verbose_name=_("Tema"),
        help_text=_("Tema del blog"),
    )
    # TODO: Añadir paneles para escoger categorías/etiquetas relacionadas y posts a destacar

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [FieldPanel("theme")],
            heading=_("Personalización"),
            icon="image",
        ),
    ]

    search_fields = BasePage.search_fields + [index.SearchField("owner")]

    subpage_types = ["BlogPostPage"]

    def get_context(self, request, *args, **kwargs):
        context = super(BlogIndexPage, self).get_context(request, *args, **kwargs)
        context["posts"] = self.get_posts()
        return context

    def get_by_owner(owner):
        """Obtiene la página a partir de su propietario"""
        return BlogIndexPage.objects.filter(owner=owner)

    def get_posts(self):
        """Devuelve las entradas del blog

        Returns:
            Array con las entradas del blog
        """
        return BlogPostPage.objects.child_of(self).live()

    @re_path(r"^tag/(?P<tag>[-\w]+)/$")
    def posts_by_tag(self, request, tag):
        """Muestra las entradas de un blog etiquetadas con una etiqueta en concreto
        Si la etiqueta tiene espacios, se reemplazan con '-'
        Arguments:
            request -- Petición realizada a la aplicación web
            tag     -- Etiqueta por la que filtrar
        """
        posts = self.get_posts().filter(tags__slug=tag)
        return self.render(request, context_overrides={"posts": posts})

    @re_path(r"^category/(?P<category>[-\w]+)/$")
    def posts_by_category(self, request, category):
        """Muestra las entradas de un blog etiquetadas con una etiqueta en concreto
        Si la etiqueta tiene espacios, se reemplazan con '-'
        Arguments:
            request -- Petición realizada a la aplicación web
            tag     -- Etiqueta por la que filtrar
        """
        posts = self.get_posts().filter(categories__blog_category_slug=category)
        return self.render(request, context_overrides={"posts": posts})

    @path("")
    def posts_list(self, request, *args, **kwargs):
        posts = self.get_posts()
        return self.render(request, context_overrides={"posts": posts})

    class Meta:
        verbose_name = _("Página de Blog")
        verbose_name_plural = _("Páginas de Blog")
        get_latest_by = "first_published_at"


class BlogPostPage(BasePage):
    """Página para las entradas de un blog de usuario."""

    page_description = _("Entrada de un blog")
    body = StreamField(BlogPostBlock())
    date = models.DateField(
        default=datetime.date.today,
        verbose_name=_("Fecha"),
        help_text=_("Fecha de la entrada"),
    )
    tags = ClusterTaggableManager(
        through="blog.BlogPostPageTag",
        blank=True,
        verbose_name=_("Etiquetas"),
        help_text=_("Las etiquetas facilitan la búsqueda de tus entradas"),
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("body"),
        FieldPanel("date"),
        MultiFieldPanel(
            [FieldPanel("tags"), InlinePanel("categories", label=_("Categorías"))],
            heading=_("Etiquetas y categorías"),
            icon="tag",
        ),
    ]
    search_fields = BasePage.search_fields + [
        index.SearchField("date"),
        index.SearchField("tags"),
        index.AutocompleteField("tags"),
        index.AutocompleteField("categories"),
    ]
    parent_page_types = ["BlogIndexPage"]
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["blog"] = self.get_parent()
        context["comments"] = self.comments.all().order_by("-created_at")
        context["tags"] = self.tags.all()
        context["categories"] = self.categories.all()
        context["form"] = CommentForm()
        return context

    class Meta:
        verbose_name = _("Entrada de blog")
        verbose_name_plural = _("Entradas de blog")
        get_latest_by = "first_published_at"


# Snippets para blogs
class Tag(TaggitTag):
    """Snippet de etiquetas."""

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        verbose_name = _("Etiqueta")
        verbose_name_plural = _("Etiquetas")


class BlogCategory(models.Model):
    """Snippet para las categorías de un blog."""

    name = models.CharField(
        max_length=255, verbose_name=_("Nombre"), help_text=_("Nombre de la categoría")
    )
    slug = models.SlugField(
        unique=True,
        max_length=80,
        verbose_name=_("Slug"),
        help_text=_("Slug de la categoría"),
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Categoría")
        verbose_name_plural = _("Categorías")


class BlogPostPageBlogCategory(models.Model):
    """Modelo que conecta las entradas de un blog con las categorías del blog."""

    page = ParentalKey(
        "blog.BlogPostPage", on_delete=models.CASCADE, related_name="categories"
    )
    blog_category = models.ForeignKey(
        "blog.BlogCategory", on_delete=models.CASCADE, related_name="posts"
    )

    panels = [
        FieldPanel("blog_category"),
    ]

    class Meta:
        unique_together = ("page", "blog_category")


class BlogPostPageTag(TaggedItemBase):
    """Modelo que conecta las entradas del blog con las etiquetas."""

    content_object = ParentalKey("blog.BlogPostPage", related_name="post_tags")
