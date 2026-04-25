from django.conf import settings
from django.db import models
from wagtail.models import PreviewableMixin, RevisionMixin, TranslatableMixin

from base.models import TimeStampedModel


# Create your models here.
class Comment(RevisionMixin, PreviewableMixin, TranslatableMixin, TimeStampedModel, models.Model):
    """Comentario en una entrada de un blog."""

    page = models.ForeignKey(
        "blog.BlogPost",
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="Página",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="comments", on_delete=models.CASCADE, verbose_name="Usuario"
    )
    content = models.TextField(max_length=150, null=False, blank=False, verbose_name="Contenido", help_text="El contenido del comentario")

    def __str__(self):
        return f'Comentario de {self.user.username} en "{self.page.title}"'

    def get_preview_template(self, request, mode_name):
        return "partials/comment.html"

    def get_preview_context(self, request, mode_name):
        return {"comment": self}
    
    class Meta(TranslatableMixin.Meta):
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
