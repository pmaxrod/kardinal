from django.shortcuts import render
from wagtail.users.views.users import UserViewSet as WagtailUserViewSet
from .forms import CustomUserCreationForm, CustomUserEditForm

# Create your views here.
class UserViewSet(WagtailUserViewSet):
    template_prefix = "users/templates/"
    def get_form_class(self, for_update=False):
        if for_update:
            return CustomUserEditForm
        return CustomUserCreationForm