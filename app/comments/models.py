from django.utils.translation import gettext as _
from django.conf import settings
from django.db import models

from base.models import TimeStampedMixin, Like


# Create your models here.
class Comment(TimeStampedMixin, models.Model):
    """Comentario en una entrada de un blog."""

    page = models.ForeignKey(
        "blog.BlogPostPage",
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name=_("Página"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name=_("Usuario"),
    )
    content = models.TextField(
        max_length=150,
        null=False,
        blank=False,
        verbose_name=_("Contenido"),
        help_text=_("El contenido del comentario"),
    )

    def liked_by_user(self, user):
        """Devuelve True si el usuario dio 'Me gusta' al comentario."""
        return self.likes.filter(comment=self, user=user).first()

    @property
    def like_count(self):
        """Devuelve el total de 'Me gusta' de un comentario."""
        return self.likes.count()

    def __str__(self):
        return _(f'Comentario de {self.user.username} en "{self.page.title}"')

    class Meta:
        verbose_name = _("Comentario")
        verbose_name_plural = _("Comentarios")


class CommentLike(Like):
    """Modelo para los 'Me gusta' de comentarios"""

    comment = models.ForeignKey(
        "comments.Comment", on_delete=models.CASCADE, related_name="likes"
    )

    def __str__(self):
        return f"Me gusta de {self.user} a {self.comment} en {self.liked_at}"
    
    class Meta:
        verbose_name = "Me Gusta (Comentarios)"
        verbose_name_plural = "Me Gustas (Comentarios)"
