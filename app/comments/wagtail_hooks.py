from django.utils.translation import gettext as _
from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet
from comments.models import Comment

class CommentViewSet(ModelViewSet):
    model = Comment
    form_fields = ["content"]
    icon = "comment"
    menu_label = _("Comentarios")
    add_to_admin_menu = True
    admin_url_namespace = "comments"
    menu_order = 300
    list_display = ["page", "user", "content", "created_at", "edited_at", "like_count"]
    list_filter = ["page", "user", "content", "created_at", "edited_at"]
    list_per_page = 50
    copy_view_enabled = False
    inspect_view_enabled = True

@hooks.register("register_admin_viewset")
def register_viewset():
    return CommentViewSet("comments")