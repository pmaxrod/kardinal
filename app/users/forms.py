from django import forms
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from wagtail.models import Site
from wagtail.users.forms import UserCreationForm, UserEditForm
from blog.models import BlogPage
from users.models import UserAppSettings

# Formularios públicos
class UserProfileForm(forms.ModelForm):
    """Formulario para el perfil del usuario"""
    class Meta:
        model = get_user_model()
        fields = ["bio"]

class UserAppSettingsForm(forms.ModelForm):
    """Formulario para la configuración del usuario"""
    class Meta:
        model = UserAppSettings
        exclude = ["user"]

class UserSignupForm(SignupForm):
    """Formulario de creación de cuenta"""
    def save(self, request):
        user = super().save(request)

        # Crear configuración del usuario
        settings = UserAppSettings(user=user)
        settings.save()
        # Crear blog del usuario
        home_page = Site.find_for_request(request).get_root
        blog_page = BlogPage(
            user=user, title=f"Blog de {user.username}", slug=user.username.lower()
        )
        blog_page.owner = user
        home_page.add_child(instance=blog_page)
        home_page.save()

        return user

# Formularios de la página de administración
class CustomUserEditForm(UserEditForm):
    """Formulario de edición de usuarios en la página de administración."""
    class Meta:
        model = get_user_model()
        fields = UserEditForm.Meta.fields | {"bio", "profile_picture"}

class CustomUserCreationForm(UserCreationForm):    
    """Formulario de creación de usuarios en la página de administración."""
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields | {"bio", "profile_picture"}