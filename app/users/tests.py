from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from wagtail.models import Page, Site
from blog.models import BlogDashboardPage, BlogIndexPage
from home.models import HomePage
from users.models import AppSettings

User = get_user_model()

# Create your tests here.

class UserSignupTestCase(TestCase):
    fixtures = ["fixtures/initial_data.json"]
    def setUp(self):
        self.username = "Pepito"
        self.email = "pepito@gmail.com"
        self.password = "contra_sena"

    def test_signup(self):
        response = self.client.post(
            reverse("account_signup"),
            data={
                "username": self.username,
                "email": self.email,
                "password1": self.password,
                "password2": self.password,
            },
        )
        user = User.objects.last()
        blog_page = BlogIndexPage.objects.get(owner=user)
        profile = AppSettings.objects.get(user=user)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(blog_page.slug, user.username)
        self.assertTrue(profile.theme, user.profile.theme)
        self.assertTrue(user.groups.first(), "Bloggers")
