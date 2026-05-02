from django import template
from django.template.defaultfilters import stringfilter
from wagtail.models import Site
from base.models import FooterText
from blog.models import BlogIndexPage, BlogPostPage
from comments.models import Comment

register = template.Library()


# Etiquetas de plantillas
@register.inclusion_tag("base/includes/footer_text.html", takes_context=True)
def get_footer_text(context):
    """Devuelve el texto que aparece en el pie de la aplicación.

    Arguments:
        context -- Contexto de la página que llama la etiqueta

    Returns:
        Diccionario con la clave "footer_text" y de valor
        el cuerpo del snippet FooterText a referenciar en
        la plantilla footer_text.html
    """
    footer_text = context.get("footer_text", "")

    if not footer_text:
        instance = FooterText.objects.filter(live=True).first()
        footer_text = instance.body if instance else ""

    return {
        "footer_text": footer_text,
    }


@register.inclusion_tag("base/includes/user_with_pfp.html")
def get_user_with_pfp(user):
    """Renderiza la plantilla user_profile.html a 
    partir del usuario que recibe como parámetro.
    
    Arguments:
        user -- Usuario cuyo perfil se quiere renderizar

    Returns:
        Diccionario con la clave "user" y de valor el usuario a 
        referenciar en la plantilla user_profile.html
    """
    return {"user": user}

@register.simple_tag(takes_context=True)
def get_site_root(context):
    """Devuelve la página raíz del sitio a partir de la petición.

    Arguments:
        context -- Contexto de la página que llama la etiqueta

    Returns:
        Página web raíz del sitio
    """
    return Site.find_for_request(context["request"]).root_page

@register.simple_tag(takes_context=True)
def comment_liked_by_user(context):
    """Comprueba si un comentario ha recibido un 'Me gusta' por parte del usuario actual
    
    Arguments:
        context -- Contexto de la página que llama la etiqueta

    Returns:
        True si el usuario actual ha dado 'Me gusta' al comentario.
        False en caso contrario.
    """
    comment = context.get("comment")
    user = context.get("request").user
    return Comment.liked_by_user(comment, user)

@register.simple_tag(takes_context=True)
def post_liked_by_user(context):
    """Comprueba si una entrada ha recibido un 'Me gusta' por parte del usuario actual
    
    Arguments:
        context -- Contexto de la página que llama la etiqueta

    Returns:
        True si el usuario actual ha dado 'Me gusta' a la entrada.
        False en caso contrario.
    """
    page = context.get("page")
    user = context.get("request").user
    return BlogPostPage.liked_by_user(page, user)

@register.simple_tag()
def get_user_blog_index_url(user):
    """Devuelve la URL del blog del usuario pasado por parámetro.
    Arguments:
        user -- Usuario cuyo perfil se quiere renderizar
    Returns:
        Devuelve el enlace al blog del usuario actual
    """
    return BlogIndexPage.objects.get(owner=user).url

# Filtros de plantillas
@register.filter
@stringfilter
def initials(value:str):
    """Devuelve las iniciales en mayúscula de una cadena.

    Arguments:
        value -- Cadena que es filtrada

    Returns:
        Cadena con solo las iniciales de value
    """
    text = ""
    for part in value.split():
        text += f"{part[0].upper()}"
    return text