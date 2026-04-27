from django.urls import path
from wagtail import hooks
from django.templatetags.static import static
from django.utils.html import format_html

from dashboard.views import CustomAccountView


@hooks.register("get_avatar_url")
def get_profile_avatar(user, size):
    return user.profile_picture


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(f'<link rel="stylesheet" href={static("css/admin.css")}>')
