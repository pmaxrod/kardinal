from users.models import UserAppSettings


def app_settings(request):
    if request.user.is_authenticated:
        settings = UserAppSettings.objects.filter(user=request.user).first()
    else:
        settings = UserAppSettings()
    return {"settings": settings}
