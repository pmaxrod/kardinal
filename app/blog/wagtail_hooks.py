from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.models import Page
from wagtail.admin.ui.tables import Column, UserColumn, RelatedObjectsColumn
from wagtail.admin.views.pages.listing import IndexView
from wagtail.admin.viewsets.pages import PageListingViewSet, PageViewSet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from blog.models import (
    BlogCategory,
    BlogIndexPage,
    BlogPage,
    Tag,
)
from dashboard.models import DashboardPage


# Viewsets de páginas
class CustomPageIndexView(IndexView):
    """Vista para las páginas."""

    model = Page

    def get_base_queryset(self):
        pages = super().get_base_queryset()
        blogger = self.request.user.groups.filter(name="Bloggers").exists()
        if blogger:
            pages = pages.filter(owner=self.request.user)
        return pages


class CustomPageViewSet(PageViewSet):
    """ViewSet de campos para las páginas del sitio web."""

    columns = PageViewSet.columns + [
        UserColumn("owner", label=_("Propietario"), sort_key="owner"),
    ]


class BlogIndexViewSet(CustomPageViewSet):
    """ViewSet de campos para los índices del blog."""

    model = BlogIndexPage
    parent_models = [DashboardPage]
    columns = CustomPageViewSet.columns + [
        Column("theme", label=_("Tema"), sort_key="theme"),
    ]


class BlogViewSet(CustomPageViewSet):
    """ViewSet de campos para las entradas del blog."""

    model = BlogPage
    parent_models = [BlogIndexPage]
    columns = CustomPageViewSet.columns + [
        RelatedObjectsColumn(
            "categories", label=_("Categorías"), sort_key="categories"
        ),
        RelatedObjectsColumn("tags", label=_("Etiquetas"), sort_key="tags"),
    ]


class BlogIndexListingViewSet(PageListingViewSet):
    """Menú de listado de blogs de usuario."""

    model = BlogIndexPage
    menu_label = _("Índice del blog")
    icon = "thumbtack"
    add_to_admin_menu = True
    columns = BlogIndexViewSet.columns
    index_view_class = CustomPageIndexView


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
    menu_order = 450
    items = (TagViewSet(), BlogCategoryViewSet())


# Viewsets de atributos de páginas
@hooks.register("register_admin_viewset")
def register_page_viewset():
    return CustomPageViewSet()


@hooks.register("register_admin_viewset")
def register_blog_index_page_viewset():
    return BlogIndexViewSet()


@hooks.register("register_admin_viewset")
def register_blog_post_page_viewset():
    return BlogViewSet()


@hooks.register("register_admin_viewset")
def register_blog_index_page_listing_viewset():
    return BlogIndexListingViewSet("blog")


# Grupos de viewsets
@hooks.register("register_admin_viewset")
def register_blog_snippets_viewset():
    return BlogSnippetsViewSetGroup()


# Hooks para evitar comportamiento irresponsable de usuarios
protected_pages = ("homepage", "dashboardPage", "blogindexpage")


@hooks.register("before_create_page")
def disable_extra_blogs(request, parent_page, page_class):
    """Impide que los usuarios puedan tener más de un blog."""
    if not request.user.is_superuser and page_class == BlogIndexPage:
        messages.error(request, "No puedes crear un blog.")
        return HttpResponseRedirect(request.headers["referer"])


@hooks.register("before_copy_page")
def disable_copy_page(request, page):
    """Bloquea el copiado de páginas."""
    messages.error(request, "No se pueden copiar páginas.")
    return HttpResponseRedirect(request.headers["referer"])


@hooks.register("before_move_page")
def disable_move_page(request, parent_page, page_class):
    """Bloquea el movimiento de páginas."""
    messages.error(request, "No se pueden mover páginas.")
    return HttpResponseRedirect(request.headers["referer"])


@hooks.register("before_unpublish_page")
def disable_unpublish_pages(request, page):
    """Impide que se puedan despublicar páginas importantes de la aplicación."""
    if not (request.user.is_superuser and page.content_type.model in protected_pages):
        messages.error(request, f"No se puede despublicar: '{page}'.")
        return HttpResponseRedirect(request.headers["referer"])


@hooks.register("before_delete_page")
def disable_delete_pages(request, page):
    """Impide que se puedan borrar páginas importantes de la aplicación."""
    if not request.user.is_superuser and (
        page.content_type.model in protected_pages or request.user != page.owner
    ):
        messages.error(request, f"No se puede borrar '{page}'.")
        return HttpResponseRedirect(request.headers["referer"])


@hooks.register("construct_explorer_page_queryset")
def only_show_owned_pages(parent_page, pages, request):
    """Limitar páginas visibles a los bloggers."""
    blogger = request.user.groups.filter(name="Bloggers").exists()
    if blogger:
        pages = pages.filter(owner=request.user)

    return pages


@hooks.register("construct_page_chooser_queryset")
def only_choose_owned_pages(pages, request):
    """Limitar las páginas a escoger a las de los propios usuarios."""
    pages = pages.filter(owner=request.user)
    return pages


@hooks.register("construct_page_listing_buttons")
def hide_page_listing_buttons(buttons, page, user, context=None):
    """Oculta las acciones sobre páginas en el listado de páginas."""
    if page.is_root:
        buttons.pop()
