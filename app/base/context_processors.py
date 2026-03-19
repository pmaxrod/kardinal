def theme(request):
    current_theme = request.session.get("theme", "system")
    return { "theme": current_theme }

def font(request):
    current_font = request.session.get("font", "sans")
    return {"font": current_font}