from django.shortcuts import render
from comments.forms import CommentForm

# Create your views here.
def create_comment(request, page):
    """Vista para crear comentarios

    Arguments:
        request -- Petición realizada a la aplicación web
    """
    context = {}
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.page = page
        comment.user = request.user
        comment.save()
        form.clean()
    return form
    #return render(request, "comments/comment_form.html", context)