from django import forms
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from wagtail.users.forms import UserCreationForm, UserEditForm, _

User = get_user_model()


# Formularios públicos
class UserProfileForm(forms.ModelForm):
    """Formulario para el perfil del usuario"""


    class Meta:
        model = User
        fields = ["bio"]


class UserSignupForm(SignupForm):
    """Formulario de creación de cuenta"""

    def save(self, request):
        user = super().save(request)
        return user


# Formularios de la página de administración
user_fields = {"username", "email", "is_superuser", "groups"}


class CustomUserEditForm(UserEditForm):
    """Formulario de edición de usuarios en la página de administración."""

    # Por algún motivo no se elminan del formulario los campos de nombre y apellidos
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        delete_fields(self.fields)

    class Meta:
        model = User
        fields = user_fields | {"is_active"}


class CustomUserCreationForm(UserCreationForm):
    """Formulario de creación de usuarios en la página de administración."""

    # Por algún motivo no se elminan del formulario los campos de nombre y apellidos
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        delete_fields(self.fields)

    class Meta:
        model = User
        fields = user_fields


def delete_fields(fields):
    """Para borrar campos en formularios que no se usan."""
    fields_to_delete = ["first_name", "last_name"]
    for field in fields_to_delete:
        del fields[field]
