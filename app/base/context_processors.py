from users.models import UserSettings


def app_settings(request):
    if request.user.is_authenticated:
        settings = UserSettings.objects.filter(user=request.user).first()
    else:
        settings = UserSettings()
    return {"settings": settings}
