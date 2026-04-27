from django import forms
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from wagtail.models import Site
from wagtail.users.forms import UserCreationForm, UserEditForm, _
from blog.models import BlogIndexPage
from users.models import AppSettings

User = get_user_model()


# Formularios públicos
class UserProfileSettingsForm(forms.ModelForm):
    """Formulario para el perfil del usuario"""


    class Meta:
        model = User
        fields = ["bio", "profile_picture"]


class AppSettingsForm(forms.ModelForm):
    """Formulario para la configuración del usuario"""

    class Meta:
        model = AppSettings
        exclude = ["user"]


class UserSignupForm(SignupForm):
    """Formulario de creación de cuenta"""

    def save(self, request):
        user = super().save(request)

        # Crear configuración del usuario
        settings = AppSettings(user=user)
        settings.save()
        # Crear blog del usuario
        root = Site.find_for_request(request).root_page
        blog = BlogIndexPage(owner=user)
        root.add_child(instance=blog)
        root.save()
        return user


# Formularios de la página de administración
user_fields = {"username", "email", "is_superuser", "groups"}
class CustomUserEditForm(UserEditForm):
    """Formulario de edición de usuarios en la página de administración."""
    # Por algún motivo no se elminan del formulario los campos de nombre y apellidos
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["first_name"]
        del self.fields["last_name"]

    class Meta:
        model = User
        fields = user_fields | {"is_active"}


class CustomUserCreationForm(UserCreationForm):
    """Formulario de creación de usuarios en la página de administración."""
    # Por algún motivo no se elminan del formulario los campos de nombre y apellidos
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["first_name"]
        del self.fields["last_name"]

    class Meta:
        model = User
        fields = user_fields
