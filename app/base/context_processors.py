def theme(request):
    current_theme = request.session.get("theme", "light")
    return { "theme": current_theme }