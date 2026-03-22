from django import template

from base.models import ThemeOption

register = template.Library()

@register.inclusion_tag("base/includes/theme_select.html", takes_context=True)
def get_theme_select(context):
    return {
        "theme_options": ThemeOption.objects.all(),
        "request": context["request"]
    }

