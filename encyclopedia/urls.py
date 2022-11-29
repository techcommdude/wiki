from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="index"),
    path("wiki/<title>", views.editPage, name="editPage"),
    path("wiki/", views.newPage, name="newPage")
]
