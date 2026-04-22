from django import forms
from allauth.account.forms import SignupForm
from wagtail.models import Site
from blog.models import BlogPage
from users.models import UserProfile, UserSettings


class UserSignupForm(SignupForm):
    # Se busca crear una página de blog asociada al usuario que se va a crear
    def save(self, request):
        user = super().save(request)

        # Crear perfil del usuario
        profile = UserProfile(user=user)
        profile.save()
        # Crear configuración del usuario
        settings = UserSettings(user=user)
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


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["user"]
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "cols": 80,
                    "rows": 10,
                    "class": "form-textarea border-2 rounded-md px-4 py-3",
                }
            ),
            "profile_picture": forms.FileInput(
                attrs={"class": "form-input border-2 rounded-md px-4 py-3"}
            ),
        }


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        exclude = ["user"]
