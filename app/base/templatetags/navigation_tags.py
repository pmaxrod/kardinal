from django import template
from django.conf import settings
from wagtail.models import Site
from base.models import FooterText, ThemeOption

register = template.Library()

@register.inclusion_tag("base/includes/footer_text.html", takes_context=True)
def get_footer_text(context):
    footer_text = context.get("footer_text", "")

    if not footer_text:
        instance = FooterText.objects.filter(live=True).first()
        footer_text = instance.body if instance else ""

    return {
        "footer_text": footer_text,
    }

@register.inclusion_tag("base/includes/user_profile.html")
def get_user_profile(user):
    return {'user': user}

@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context["request"]).root_page
