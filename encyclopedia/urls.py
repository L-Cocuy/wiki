from encyclopedia.util import delete_entry
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("edit", views.edit, name="edit"),
    path("delete", views.delete_entry, name="delete"),
    path("random_page", views.random_page, name="random_page"),
    path("<str:entry_title>", views.display_entry, name="display_entry")
]
