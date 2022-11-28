import re
from django import forms
from django.http import HttpResponse
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


class entryForm(forms.Form):
    #what is the point of this?
    existingEntry = forms.Textarea()


def displayEntry(request, displayEntry):

    # Use this to retrieve the entry to display.  Put it in a function?
    entryContents = util.get_entry(displayEntry)

# Trying to display the initial value of the form.

    if entryContents != None:

        findInstance = re.findall(displayEntry, entryContents, re.IGNORECASE)
        displayEntry = findInstance[0]

    else:
        return render(request, "encyclopedia/error.html", {
            "displayEntry": displayEntry
        })

    if request.method == 'GET':
        print("Get")

        form = entryForm()

        return render(request, "encyclopedia/entry.html", {'form': form, "displayEntry": displayEntry, "entryContents": entryContents}
                      )

    # Need to handle request.post.
