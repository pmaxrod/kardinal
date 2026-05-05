from django import template
from django.template.defaultfilters import stringfilter
from wagtail.models import Site
from base.models import FooterText
from blog.models import BlogIndexPage, BlogPostPage
from comments.models import Comment

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
def get_user_with_pfp(user):
    """Devuelve el nombre del usuario junto con su foto de perfil
    a partir del usuario que recibe como parámetro."""
    return {"user": user}

@register.inclusion_tag("base/includes/breadcrumbs.html", takes_context=True)
def get_breadcrumbs(context):
    """Devuelve un componente breadcrumb para navegar a través de una jerarquía de páginas."""
    page = context.get("page")
    ancestors = page.get_ancestors()

    return {"page": page, "ancestors": ancestors}


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
    return BlogPostPage.liked_by_user(page, user)


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
