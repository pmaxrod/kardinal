from django.urls import include, path
from blog import views

urlpatterns = [
    path("add_post/", views.add_post_view, name="add_post"),
]
