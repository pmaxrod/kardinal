from django.apps import AppConfig
from wagtail.users.apps import WagtailUsersAppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    default = True


class CustomUsersAppConfig(WagtailUsersAppConfig):
    user_viewset = "users.viewsets.UserViewSet"