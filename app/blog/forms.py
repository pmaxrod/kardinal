from django.db import models
from django import forms
from blog.models import PostPage

"""
class PostForm(forms.Form):
    body = forms.TextInput
    tags = forms.Textarea
"""
class PostForm(forms.ModelForm):
    class Meta:
        model = PostPage
        fields = ["body","tags"]
        #exclude = ["created_at"]
