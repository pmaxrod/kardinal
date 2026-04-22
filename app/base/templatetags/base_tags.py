from django import template
from django.contrib.auth.models import User
from wagtail.models import Site
from base.models import FooterText
from django.template.defaultfilters import stringfilter

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


@register.inclusion_tag("base/includes/user_profile.html")
def get_user_profile(user: User):
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