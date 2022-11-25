from django.http import HttpResponse
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def displayEntry(request, entry):

    if util.get_entry(entry):
        return HttpResponse(f"Hello, {entry}!")
    else:
        return HttpResponse(f"Not in the list!")
