from django import template
from django.template.defaultfilters import stringfilter
from wagtail.models import Site
from base.models import FooterText, SocialMediaLink
from blog.models import BlogIndexPage, BlogPage
from comments.models import Comment
from base.models import AppFontFamilies, AppThemes

register = template.Library()


# Etiquetas con plantillas asociadas
@register.inclusion_tag("base/includes/footer_text.html", takes_context=True)
def get_footer_text(context):
    """Devuelve el valor del primer registro del snippet FooterText."""
    footer_text = context.get("footer_text", "")

    if not footer_text:
        instance = FooterText.objects.filter(live=True).first()
        footer_text = instance.body if instance else ""

    return {
        "footer_text": footer_text,
    }


@register.inclusion_tag("base/includes/user_with_pfp.html")
def get_user_with_pfp(user, show_bio=False):
    """Devuelve el nombre del usuario junto con su foto de perfil
    a partir del usuario que recibe como parámetro.

    La biografía se puede mostrar de forma opcional.
    """
    return {"user": user, "show_bio": show_bio}


@register.inclusion_tag("base/includes/breadcrumbs.html", takes_context=True)
def get_breadcrumbs(context):
    """Devuelve un componente breadcrumb para navegar a través de una jerarquía de páginas."""
    page = context.get("page")
    ancestors = page.get_ancestors()

    return {"page": page, "ancestors": ancestors}


@register.inclusion_tag("base/includes/social_media_links.html", takes_context=True)
def get_social_media_links(context):
    """Devuelve los enlaces de redes sociales."""
    links = context.get("links")
    if not links:
        links = SocialMediaLink.objects.filter(live=True)

    return {"links": links}


@register.inclusion_tag("base/includes/theme_selector.html", takes_context=True)
def app_theme_selector(context):
    """Devuelve el selector de temas de la aplicación."""
    themes = AppThemes.choices
    return {"themes": themes}


@register.inclusion_tag("base/includes/font_families_selector.html", takes_context=True)
def app_font_family_selector(context):
    """Devuelve el selector de tipos de fuente de la aplicación."""
    families = AppFontFamilies.choices
    return {"families": families}


@register.inclusion_tag("blog/includes/post_categories.html", takes_context=True)
def post_categories(context):
    """Devuelve las categorías de una entrada de un blog."""
    request = context.get("request")
    post = context.get("page").specific
    blog = post.get_parent().specific
    categories = post.categories.all()
    return {"request": request, "blog": blog, "categories": categories}


@register.inclusion_tag("blog/includes/post_tags.html", takes_context=True)
def post_tags(context):
    """Devuelve las etiquetas de una entrada de un blog."""
    request = context.get("request")
    post = context.get("page").specific
    blog = post.get_parent().specific
    tags = post.tags.all()
    return {"request": request, "blog": blog, "tags": tags}


# Etiquetas de plantillas sin plantilla asociadas
@register.simple_tag(takes_context=True)
def get_site_root(context):
    """Devuelve la página raíz del sitio a partir de la petición al sitio web."""
    return Site.find_for_request(context["request"]).root_page


@register.simple_tag(takes_context=True)
def comment_liked_by_user(context):
    """Comprueba si un comentario ha recibido un 'Me gusta' por parte del usuario actual."""
    comment = context.get("comment")
    user = context.get("request").user
    return Comment.liked_by_user(comment, user)


@register.simple_tag(takes_context=True)
def post_liked_by_user(context):
    """Comprueba si una entrada ha recibido un 'Me gusta' por parte del usuario actual."""
    page = context.get("page")
    user = context.get("request").user
    return BlogPage.liked_by_user(page, user)


@register.simple_tag()
def get_user_blog_index_url(user):
    """Devuelve la URL del blog del usuario pasado por parámetro."""
    return BlogIndexPage.objects.get(owner=user).url


# Filtros de plantillas
@register.filter
@stringfilter
def initials(value: str):
    """Devuelve las iniciales en mayúscula de una cadena."""
    text = ""
    for part in value.split():
        text += f"{part[0].upper()}"
    return text
