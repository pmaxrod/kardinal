def theme(request):
    current_theme = request.session.get("theme", "system")
    return { "theme": current_theme }