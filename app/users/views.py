from django.shortcuts import render, redirect
from users.forms import UserAppSettingsForm, UserProfileForm
from users.models import UserAppSettings


# Create your views here.
def update_user_profile(request):
    instance = request.user

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            user_settings = form.save()
            user_settings.user = request.user
            user_settings.save()
            return redirect("/profile")
    else:
        form = UserProfileForm(instance=instance)

    context = {"form": form}
    return render(request, "update_user_profile.html", context)


def update_user_settings(request):
    instance = UserAppSettings.objects.get(user=request.user)

    if request.method == "POST":
        form = UserAppSettingsForm(request.POST, instance=instance)

        if form.is_valid():
            user_settings = form.save()
            user_settings.user = request.user
            user_settings.save()
            return redirect("/settings")
    else:
        form = UserAppSettingsForm(instance=instance)

    context = {"form": form}
    return render(request, "update_user_settings.html", context)
