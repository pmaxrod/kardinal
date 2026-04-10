from django.urls import include, path
from users import views

urlpatterns = [
    path("profile/", views.user_profile_form, name="user_profile_form"),
    path("profile/<str:username>/", views.get_user_profile, name="get_user_profile"),
]
