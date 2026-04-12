from django.urls import include, path
from users import views

urlpatterns = [
    path("profile/", views.user_profile_form, name="user_profile_form"),
    path("settings/", views.update_user_settings, name="update_user_settings"),
]
