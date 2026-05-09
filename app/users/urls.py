from django.urls import path
from users import views

urlpatterns = [
    path("profile/", views.update_user_profile, name="update_user_profile"),
    path("settings/theme/", views.update_app_theme, name="update_user_theme"),
    path("settings/font_family/", views.update_app_font_family, name="update_user_font_family"),
]
