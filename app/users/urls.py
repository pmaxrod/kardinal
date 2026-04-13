from django.urls import include, path
from users import views

urlpatterns = [
    path("profile/", views.update_user_profile, name="update_user_profile"),
    path("settings/", views.update_user_settings, name="update_user_settings"),
]
