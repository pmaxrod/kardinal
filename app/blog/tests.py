from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase
from blog.models import BlogIndexPage, BlogPage
from dashboard.models import DashboardPage
from home.models import HomePage


# Create your tests here.
class BlogPagesTest(WagtailPageTestCase):
    fixtures = ["fixtures/initial_data.json"]

    @classmethod
    def setUpTestData(cls):
        cls.dashboard = DashboardPage.objects.first()
        cls.blog_index = BlogIndexPage.objects.first()

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(DashboardPage, {BlogIndexPage})
        self.assertAllowedSubpageTypes(BlogIndexPage, {BlogPage})

    def test_blogindexpage_routing(self):
        self.assertPageIsRoutable(self.blog_index, "/category/programacion/")
        self.assertPageIsRoutable(self.blog_index, "/tag/miprimerpost/")


class BlogIndexPageTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(self):
        root = Page.get_first_root_node()
        Site.objects.create(
            hostname="testserver",
            root_page=root,
            is_default_site=True,
            site_name="testserver",
        )
        home = HomePage(body="Contenido de prueba")
        root.add_child(instance=home)
        self.page = BlogIndexPage()
        home.add_child(instance=self.page)

    def test_get(self):
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
