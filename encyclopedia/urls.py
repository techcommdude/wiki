from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="index"),
    path("wiki/<str:displayEntry>", views.displayEntry, name="displayEntry")
]
