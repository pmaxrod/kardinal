from django.test import TestCase
from django.urls import reverse
from blog.models import BlogPage

# Create your tests here.
class UserSignupTestCase(TestCase):
    def setUp(self):
        self.username = "Pepito"
        self.email = "pepito@gmail.com"
        self.password = "contra_sena"
    
    def test_signup(self):
        response = self.client.post(reverse('account_signup'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })

        self.assertEqual(response.status_code, 302)
        blog_page = BlogPage.objects.get(owner__username=self.username.lower())
        self.assertTrue(blog_page.slug, 'pepito')
        self.assertTrue(blog_page.title, 'Blog de Pepito')