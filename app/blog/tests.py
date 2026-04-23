from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase
from blog.models import BlogPage
from home.models import HomePage

# Create your tests here.
class BlogPageTest(WagtailPageTestCase):
    def setUpTestData(self):
        root = Page.get_first_root_node()
        Site.objects.create(
            hostname="testserver",
            root_page=root,
            is_default_site=True,
            site_name="testserver"
        )
        home = HomePage(hero_test="Test", body="Contenido de prueba")
        root.add_child(instance=home)
        self.page = BlogPage()
        home.add_child(instance=self.page)