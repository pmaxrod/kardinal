from wagtail import hooks
from django.templatetags.static import static
from django.utils.html import format_html


@hooks.register("insert_global_admin_css")
def global_admin_css():
    """Inserta CSS para las páginas de administración."""
    return format_html(f'<link rel="stylesheet" href={static("css/admin.css")}>')


@hooks.register("register_icons")
def register_icons(icons):
    """Registra iconos para las páginas de administración."""
    icons.append("wagtailadmin/icons/blogindex.svg")
    icons.append("wagtailadmin/icons/blogpost.svg")
    return icons

@hooks.register("construct_main_menu")
def hide_menu_options(request, menu_items):
    """Oculta opciones solo para el administrador a los bloggers."""
    admin_items = ["explorer", "reports", "settings"]
    if request.user.groups.filter(name__in=["Bloggers"]):
        menu_items[:] = [item for item in menu_items if item.name not in admin_items]