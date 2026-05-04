from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
<<<<<<< HEAD
    default = True


class CustomUsersAppConfig(WagtailUsersAppConfig):
    user_viewset = "users.viewsets.UserViewSet"
=======

    def ready(self):
        import users.signals
>>>>>>> da7d56c (Creadas signals para eventos al registrarse el usuario)
