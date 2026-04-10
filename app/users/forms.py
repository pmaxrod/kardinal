from django import forms
from allauth.account.forms import SignupForm
from wagtail.models import Site
from blog.models import BlogPage
from users.models import UserProfile

class UserSignupForm(SignupForm):
    # Se busca crear una página de blog asociada al usuario que se va a crear
    def save(self, request):
        user = super().save(request)
        
        # Crear perfil del usuario
        profile = UserProfile(user=user)
        profile.save()
        # Crear configuración del usuario
        #settings = UserSettings(user=user)
        #settings.save()
        # Crear blog del usuario
        home_page = Site.find_for_request(request).get_root
        blog_page = BlogPage(user=user, title=f"Blog de {user.username}", slug=user.username.lower())
        blog_page.owner = user
        home_page.add_child(instance=blog_page)

        home_page.save()

        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["user"]