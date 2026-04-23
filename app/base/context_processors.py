from users.models import AppSettings


def app_settings(request):
    if request.user.is_authenticated:
        settings = AppSettings.objects.filter(user=request.user).first()
    else:
        settings = AppSettings()
    return {"settings": settings}
