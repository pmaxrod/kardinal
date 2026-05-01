from django.urls import path
from comments import views

urlpatterns = [
    path("add/<int:pk>/", views.add_page_comment, name="add_comment"),
    path("edit/<int:pk>/", views.edit_comment, name="edit_comment"),
    path("delete/<int:pk>/",views.delete_comment, name="delete_comment"),
    path("like/<int:pk>/", views.like_comment, name="like_comment")
]
