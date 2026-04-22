# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from wagtail.models import Page
from comments.forms import CommentForm
from comments.models import Comment

@login_required
@require_http_methods(['POST'])
def add_page_comment(request, slug):
    """Añade un comentario a la página.

    Arguments:
        request -- Petición realizada a la página web
        slug -- Slug de la página que se comenta

    Returns:
        Respuesta HTTP con el comentario añadido
    """
    form = CommentForm(request.POST)
    page = Page.objects.filter(slug=slug).first().specific
    form.initial['user'] = request.user
    form.initial['page'] = page
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.page = page
        comment.save()
        context = {'comment': comment}
        return render(request, "partials/comment.html", context)

@login_required
@require_http_methods(['GET', 'POST'])
def edit_comment(request, pk):
    """Edita un comentario.

    Arguments:
        request -- Petición realizada a la página web
        pk -- Clave primaria de la base de datos

    Returns:
       Comentario editado con petición POST o el formulario de edición con petición GET
    """
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    form = CommentForm(instance=comment)
    context = {'form': form, 'comment': comment}
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            context = {'comment': comment, 'form': form}
            messages.success(request, "El comentario se ha podido editar con éxito.")
            return render(request, "partials/comment.html", context)
        else:
            messages.error(request, "El comentario no se ha podido editar.")
    elif request.method == "GET":
        return render(request, "partials/edit_comment_form.html", context)
    
@login_required
@require_http_methods(['GET', 'DELETE'])    
def delete_comment(request, pk):
    """Borra un comentario.

    Arguments:
        request -- Petición realizada a la página web
        pk -- Clave primaria de la base de datos

    Returns:
        Respuesta vacía si es una petición DELETE o el mensaje de confirmación con petición GET
    """
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "DELETE":
        comment.delete()
        response = HttpResponse(status=204)
        response['HX-Trigger'] = 'delete-comment'
        messages.success(request, "El comentario se ha borrado con éxito.")
        return response
    elif request.method == "GET":
        return render(request, "partials/delete_comment_form.html", {'comment': comment})
