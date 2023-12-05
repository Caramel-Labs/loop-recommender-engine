from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("like/", views.handle_like, name="handle_like"),
    path("bookmark/", views.handle_bookmark, name="handle_bookmark"),
]
