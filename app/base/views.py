from django.shortcuts import redirect
from django.views import View

class ToggleThemeView(View):
    def post(self, request, *args, **kwargs):
        theme = request.POST.get('theme')
        if theme in ['light', 'dark', 'system']:
            request.session["theme"] = theme
        #return redirect(request.META.get("HTTP_REFERER", "users.profile"))
        return redirect(request.META.get("HTTP_REFERER"))