from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from wagtail.models import Site
from blog.models import BlogDashboardPage, BlogIndexPage
from users.models import AppSettings

User = get_user_model()


@receiver(user_signed_up, sender=User)
def create_settings(request, user, **kwargs):
    """Señal enviada para crear la configuración al registrarse el usuario."""
    settings = AppSettings(user=user)
    settings.save()


@receiver(user_signed_up, sender=User)
def create_blog_index(request, user, **kwargs):
    """Señal enviada para crear el blog del usuario al registrarse."""
    blog = BlogIndexPage(
        owner=user, title=f"Blog de {user.username}", slug=slugify(user.username)
    )
    root = Site.find_for_request(request).root_page
    dashboard = root.get_children().type(BlogDashboardPage).first()
    dashboard.add_child(instance=blog)
    dashboard.save()

@receiver(user_signed_up, sender=User)
def add_blogger(request, user, **kwargs):
    """Señal enviada para que al registrarse se le asigne el grupo Blogger."""
    group = Group.objects.get(name="Bloggers")
    user.groups.add(group)