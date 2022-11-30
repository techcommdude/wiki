from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="index"),
    path("wiki/<str:title>", views.displayPage, name="displayPage"),
    path("editPage/<str:title>", views.editPage, name="editPage"),
    path("newEntry", views.newPage, name="newPage"),
    path("randomEntry", views.randomPage, name="randomPage")

]
