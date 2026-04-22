from django.shortcuts import render

from blog.forms import PostForm


# Create your views here.
def add_post_view(request):
    context = {}
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
    context["form"] = form
    return render(request, "blog/add_post_page.html", context)
