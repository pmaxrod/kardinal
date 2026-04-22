from comments.models import Comment
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet


class CommentViewSet(SnippetViewSet):
    """ViewSet de comentarios en la interfaz de administrador de Wagtail"""

    model = Comment
    menu_label = "Comentarios de posts"
    menu_order = 300
    add_to_admin_menu = True
    admin_url_namespace = "comments"

    icon = "comment"
    list_display = ["page", "user", "content", "created_at", "edited_at"]
    list_per_page = 50
    copy_view_enabled = False
    inspect_view_enabled = True
    list_filter = ["page", "user", "content", "created_at", "edited_at"]
    panels = [
        FieldPanel("page"),
        FieldPanel("user"),
        FieldPanel("content"),
    ]


register_snippet(CommentViewSet)
