from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.forms import UserProfileForm, UserSettingsForm
from users.models import UserSettings

# Create your views here.
def user_profile_form(request):
    context = {}
    form = UserProfileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    
    context["form"] = form
    return render(request, "user_profile_form.html", context)

def update_user_settings(request):
    instance = UserSettings.objects.get(user=request.user)

    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=instance)

        if form.is_valid():
            user_settings = form.save()
            user_settings.user = request.user
            user_settings.save()
            return redirect("/settings")
    else:
        form = UserSettingsForm(instance=instance)

    context = {'form': form}
    return render(request, "update_user_settings.html", context)
