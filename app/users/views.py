from django.http import HttpResponse
from base.utils import set_cookie


# Create your views here.
def update_app_theme(request):
    """Guarda las preferencias del tema del usuario."""
    response = HttpResponse()
    set_cookie(response, "theme", request.POST.get('theme'))
    response.headers["HX-Redirect"] = request.headers["referer"]
    return response


def update_app_font_family(request):
    """Guarda las preferencias del tipo de fuente del usuario."""
    response = HttpResponse()
    set_cookie(response, "font_family", request.POST.get('font_family'))
    response.headers["HX-Redirect"] = request.headers["referer"]
    return response