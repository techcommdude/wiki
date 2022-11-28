import re
from django.http import HttpResponse
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def displayEntry(request, displayEntry):

    # Use this to retrieve the entry to display.  Put it in a function?
    entryContents = util.get_entry(displayEntry)

    if entryContents != None:

        x = re.findall(displayEntry, entryContents, re.IGNORECASE)

        return render(request, "encyclopedia/entry.html", {
            "displayEntry": x[0]
        })

    else:
        return render(request, "encyclopedia/error.html", {
            "displayEntry": displayEntry
        })
