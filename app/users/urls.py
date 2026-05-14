from django.urls import path
from users import views

urlpatterns = [
    path("settings/theme/", views.update_app_theme, name="update_user_theme"),
    path("settings/font_family/", views.update_app_font_family, name="update_user_font_family"),
    path("follow/<int:pk>/", views.follow_user, name="follow_user")
]
