from wagtail.users.views.users import UserViewSet as WagtailUserViewSet
from users.forms import CustomUserCreationForm, CustomUserEditForm

class UserViewSet(WagtailUserViewSet):
    template_prefix = "users/"

    def get_form_class(self, for_update=False):
        if for_update:
            return CustomUserEditForm
        return CustomUserCreationForm