from django.utils.translation import gettext as _
from wagtail import hooks
from wagtail.admin.ui.tables import Column, UserColumn, RelatedObjectsColumn
from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.viewsets.base import ViewSetGroup
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from blog.models import BlogCategory, BlogIndexPage, BlogPostPage, Tag


# Viewsets de páginas
class BlogIndexListingViewSet(PageListingViewSet):
    """Listado de blogs de usuario."""

    model = BlogIndexPage
    menu_label = _("Blogs de usuarios")
    icon = "thumbtack"

    columns = PageListingViewSet.columns + [
        UserColumn("owner", label=_("Propietario"), sort_key="owner"),
        Column("theme", label=_("Tema"), sort_key="theme"),
    ]


class BlogPostListingViewSet(PageListingViewSet):
    """Listado de entradas de blog."""

    model = BlogPostPage
    menu_label = _("Entradas de blog")
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

    menu_label = _("Páginas de blogs")
    menu_icon = "blogindex"
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
