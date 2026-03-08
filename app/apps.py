from wagtail.users.apps import WagtailUsersAppConfig

class CustomUsersAppConfig(WagtailUsersAppConfig):
    user_viewset = "users.viewset.UserViewSet"