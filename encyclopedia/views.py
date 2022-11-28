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

    # existingEntry = forms.Textarea(attrs={'rows':3, 'cols':5})

    existingEntry = forms.CharField(widget=forms.Textarea)



def displayEntry(request, displayEntry):



    # Use this to retrieve the entry to display.  Put it in a function?
    entryContents = util.get_entry(displayEntry)
    form = entryForm(initial={'entryContents': entryContents})
    # form.existingEntry = entryContents


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



        # return render(request, "encyclopedia/entry.html", {'form': form, "displayEntry": displayEntry, "entryContents": entryContents}
        #               )

        return render(request, "encyclopedia/entry.html", {'form': form, "displayEntry": displayEntry}
                      )

    # Need to handle request.post.
