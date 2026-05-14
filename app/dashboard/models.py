from django.shortcuts import render
from django.urls import resolve
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.routable_page.models import RoutablePageMixin, path, re_path
from base.models import BasePage
from blog.models import BlogPage

# Create your models here.


class DashboardPage(RoutablePageMixin, BasePage):
    """Página que contiene las bandejas de entradas."""

    page_description = _("Página padre de todos los blogs")

    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.BlogIndexPage"]
    max_count_per_parent = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        url_name = resolve(request.path_info).url_name
        if self.follows_feed.__str__ == url_name:
            tab = "follows"
        elif self.tags_feed.__str__ == url_name:
            tab = "tags"
        else:
            tab = "follows"
        context["active_tab"] = tab
        return context
    
    @path("feed/follows/")
    def follows_feed(self, request):
        follows_feed = BlogPage.get_published_pages(BlogPage).filter(
            owner__in=request.user.follows.all()
        )
        return render(
            request,
            "dashboard/partials/follows_feed.html",
            {"page": self, "follows_feed": follows_feed,},
        )

    @path("feed/tags/")
    def tags_feed(self, request):
        return render(request, "dashboard/partials/tags_feed_tab.html", {"page": self})

    @re_path(r"^search/tags/$")
    def search_tags(self, request):
        tags = request.POST.get("tags").split(" ")
        tags_feed = (
            BlogPage.objects.public()
            .live()
            .filter(tags__slug__in=tags)
            .distinct()
            .order_by("-last_published_at")
        )
        return render(
            request,
            "dashboard/partials/tags_feed.html",
            context={"page": self, "tags_feed": tags_feed, "tags": tags, "active_tab": "tags"},
        )

    class Meta:
        verbose_name = _("Página de listado de blogs")
        verbose_name_plural = _("Páginas de listado de blogs")
