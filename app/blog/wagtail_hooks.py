from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from wagtail import hooks
from wagtail.admin.ui.tables import Column, UserColumn, RelatedObjectsColumn
from wagtail.admin.views.pages.listing import IndexView
from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.viewsets.base import ViewSetGroup
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from blog.models import BlogCategory, BlogIndexPage, BlogPostPage, Tag


# Viewsets de páginas
class BlogIndexView(IndexView):
    """Vista para los índices de blogs."""
    model = BlogIndexPage

    def get_base_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_base_queryset()
        else:
            pages = (
                self.model.objects.filter(depth__gt=1)
                .filter(owner=self.request.user)
                .values_list("pk", flat=True)
            )
            pages = self.annotate_queryset(pages)
            return pages

class BlogPostView(IndexView):
    """Vista para las entradas de blog."""
    model = BlogPostPage

    def get_base_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_base_queryset()
        else:
            pages = (
                self.model.objects.filter(depth__gt=1)
                .filter(owner=self.request.user)
                .values_list("pk", flat=True)
            )
            pages = self.annotate_queryset(pages)
            return pages
        
class BlogIndexListingViewSet(PageListingViewSet):
    """Listado de blogs de usuario."""

    model = BlogIndexPage
    menu_label = _("Índice del blog")
    icon = "thumbtack"
    index_view_class = BlogPostView

    columns = PageListingViewSet.columns + [
        UserColumn("owner", label=_("Propietario"), sort_key="owner"),
        Column("theme", label=_("Tema"), sort_key="theme"),
    ]


class BlogPostListingViewSet(PageListingViewSet):
    """Listado de entradas de blog."""

    model = BlogPostPage
    menu_label = _("Entradas del blog")
    icon = "blogpost"

    columns = PageListingViewSet.columns + [
        UserColumn("owner", label=_("Propietario"), sort_key="owner"),
        RelatedObjectsColumn(
            "categories", label=_("Categorías"), sort_key="categories"
        ),
        RelatedObjectsColumn("tags", label=_("Etiquetas"), sort_key="tags"),
    ]


class BlogPagesViewSetGroup(ViewSetGroup):
    """Agrupador de páginas asociadas a blogs."""

    menu_label = _("Blog")
    menu_icon = "blogindex"
    menu_order = 200
    items = (BlogIndexListingViewSet("blogs"), BlogPostListingViewSet("blogposts"))


# Viewsets de snippets
class TagViewSet(SnippetViewSet):
    model = Tag
    menu_label = _("Etiquetas")
    menu_icon = "tag"
    list_display = ["name", "slug"]
    list_per_page = 50
    copy_view_enabled = False
    inspect_view_enabled = True
    admin_url_namespace = "tags"
    base_url_path = "blog/tags"


class BlogCategoryViewSet(SnippetViewSet):
    model = BlogCategory
    menu_label = _("Categorías de blog")
    menu_icon = "folder-inverse"
    list_display = ["name", "slug"]
    list_per_page = 50
    copy_view_enabled = False
    inspect_view_enabled = True
    admin_url_namespace = "blog_categories"
    base_url_path = "blog/categories"


class BlogSnippetsViewSetGroup(SnippetViewSetGroup):
    """Agrupador de etiquetas y categorías."""

    menu_label = _("Categorización")
    menu_icon = "snippet"
    items = (TagViewSet(), BlogCategoryViewSet())


@hooks.register("register_admin_viewset")
def register_blog_viewset():
    return BlogPagesViewSetGroup()


@hooks.register("register_admin_viewset")
def register_blog_snippets_viewset():
    return BlogSnippetsViewSetGroup()


# Hooks para evitar comportamiento irresponsable de usuarios
protected_pages = ("homepage", "blogdashboardpage", "blogindexpage")


@hooks.register("before_create_page")
def disable_extra_blogs(request, parent_page, page_class):
    """Impide que los usuarios puedan tener más de un blog."""
    if page_class == BlogIndexPage:
        has_blog = page_class.objects.filter(owner=request.user).exists()
        if has_blog:
            messages.error(request, "No se puede tener más de un blog.")
            return HttpResponseRedirect(request.headers["referer"])


@hooks.register("before_copy_page")
def disable_copy_page(request, page):
    """Bloquea el copiado de páginas."""
    messages.error(request, "No se pueden copiar páginas.")
    return HttpResponseRedirect(request.headers["referer"])


@hooks.register("before_unpublish_page")
def disable_unpublish_pages(request, page):
    """Impide que se puedan despublicar páginas importantes de la aplicación."""
    if page.content_type.model in protected_pages:
        messages.error(request, f"No se puede despublicar: '{page}'.")
        return HttpResponseRedirect(request.headers["referer"])


@hooks.register("before_delete_page")
def disable_delete_pages(request, page):
    """Impide que se puedan borrar páginas importantes de la aplicación."""
    if page.content_type.model in protected_pages:
        messages.error(request, f"No se puede borrar '{page}'.")
        return HttpResponseRedirect(request.headers["referer"])
