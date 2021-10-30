from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random_title", views.random_title, name="random_title"),
    path("wiki/<str:title>", views.entry, name="wiki"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("edit/<str:title>",views.edit, name="edit")


]
