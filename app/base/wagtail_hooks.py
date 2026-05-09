from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from base.models import FooterText, SocialMediaLink

# Viewsets de snippets
class FooterTextViewSet(SnippetViewSet):
    """Menú del snippet del texto del pie."""
    model = FooterText
    menu_label = _("Texto del pie")
    menu_icon = "arrow-down"
    list_per_page = 1
    copy_view_enabled = False
    inspect_view_enabled = False
    admin_url_namespace = "footer-text"
    base_url_path = "base/footer-text"

class SocialMediaLinkViewSet(SnippetViewSet):
    """Menú del snippet de enlaces de redes sociales."""
    model = SocialMediaLink
    menu_label = _("Enlaces de redes sociales")
    menu_icon = "link"
    list_per_page = 5
    copy_view_enabled = False
    inspect_view_enabled = False
    admin_url_namespace = "social-media"
    base_url_path = "base/social-media"

class BaseSnippetViewSetGroup(SnippetViewSetGroup):
    """Agrupador de snippets de configuración global."""
    menu_label = _("Global")
    menu_icon = "globe"
    menu_order = 600
    items = (FooterTextViewSet(), SocialMediaLinkViewSet())

@hooks.register("register_admin_viewset")
def register_base_snippets_viewset():
    return BaseSnippetViewSetGroup()

@hooks.register("construct_page_chooser_queryset")
def only_choose_owned_images(images, request):
    """Limitar las imágenes a escoger a las de los propios usuarios."""
    images = images.filter(uploaded_by_user=request.user)
    return images