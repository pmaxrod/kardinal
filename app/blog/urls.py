from django.urls import include, path
from blog import views

urlpatterns = [
    path("blog/<str:user>/", views.blog_page_view, name="user_blog"),
    path("add_post/", views.add_post_view, name="add_post")
]
