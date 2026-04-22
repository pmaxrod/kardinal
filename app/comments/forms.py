from django import forms
from django.urls import reverse
from comments.models import Comment


class CommentForm(forms.ModelForm):
    """Formulario para crear comentarios mediante el modelo Comment."""

    class Meta:
        model = Comment
        fields = ["content"]