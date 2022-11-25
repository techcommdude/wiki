from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="index"),
    path("wiki", views.index, name="index"),
    path("wiki/<str:entry>", views.displayEntry, name="entry")
]
