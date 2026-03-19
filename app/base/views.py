from django.shortcuts import redirect
from django.views import View
from base.models import ThemeOption

class ToggleThemeView(View):
    def post(self, request, *args, **kwargs):
        theme = request.POST.get('theme')
#        themes = ["system", "light", "dark"]
        themes = ThemeOption.objects.values_list("value", flat=True)
        if theme in themes:
            request.session["theme"] = theme
        #return redirect(request.META.get("HTTP_REFERER", "users.profile"))
        return redirect(request.META.get("HTTP_REFERER"))

class ChangeFontView(View):
    def post(self, request, *args, **kwargs):
        font = request.POST.get('font')
        if font in ['font-sans', 'font-serif']:
            request.session["font"] = font
        return redirect(request.META.get("HTTP_REFERER"))