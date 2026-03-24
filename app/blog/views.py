from django.shortcuts import render

from blog.models import PostPage, BlogPage
from blog.forms import PostForm
from users.models import UserProfile

# Create your views here.
def blog_page_view(request, user):
    blog_page = BlogPage.objects.get(user__username=user)
    return render(request, "blog/blog_page.html", {"page": blog_page})

def add_post_view(request):
    context = {}
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
    context["form"] = form
    return render(request, "blog/add_post_page.html", context)