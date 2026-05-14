from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from base.utils import set_cookie


User = get_user_model()
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

@login_required
@require_http_methods(["POST"])
def follow_user(request, pk):
    follow_user = User.objects.get(pk=pk)
    user = request.user
    if user.is_following(follow_user):
        user.unfollow(follow_user)
    else:
        user.follow(follow_user)

    return render(request, "users/partials/user_follows.html", context={"user": follow_user, "current_user": user})