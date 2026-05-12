from django.utils.translation import gettext_lazy as _
from base.models import BasePage
from blog.models import BlogPage

# Create your models here.


class DashboardPage(BasePage):
    """Página que contiene las bandejas de entradas."""

    page_description = _("Página padre de todos los blogs")

    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.BlogIndexPage"]
    max_count_per_parent = 1

    def get_context(self, request, *args, **kwargs):
        context = super(DashboardPage, self).get_context(request, *args, **kwargs)
        context["feed"] = BlogPage.objects.filter(owner=request.user).live().public()
        return context

    class Meta:
        verbose_name = _("Página de listado de blogs")
        verbose_name_plural = _("Páginas de listado de blogs")
