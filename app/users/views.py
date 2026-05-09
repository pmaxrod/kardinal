from django.http import HttpResponse
from django.shortcuts import render, redirect
from base.utils import set_cookie
from users.forms import UserProfileSettingsForm


# Create your views here.
def update_user_profile(request):
    instance = request.user

    if request.method == "POST":
        form = UserProfileSettingsForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form.save()
            return redirect("/profile")
    else:
        form = UserProfileSettingsForm(instance=instance)

    context = {"form": form}
    return render(request, "update_user_profile.html", context)


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