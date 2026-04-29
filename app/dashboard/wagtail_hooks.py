from wagtail import hooks
from django.templatetags.static import static
from django.utils.html import format_html


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(f'<link rel="stylesheet" href={static("css/admin.css")}>')


@hooks.register("register_icons")
def register_icons(icons):
    icons.append("wagtailadmin/icons/blogindex.svg")
    icons.append("wagtailadmin/icons/blogpost.svg")
    return icons
