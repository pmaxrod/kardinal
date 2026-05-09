from base.models import AppFontFamilies, AppThemes


def app_settings(request):
    theme = request.COOKIES.get("theme", AppThemes.DEFAULT)
    font_family = request.COOKIES.get(
        "font_family", AppFontFamilies.SANS_SERIF
    )
    return {"theme": theme, "font_family": font_family}
