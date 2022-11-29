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

class NewPageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

class EditPageForm(forms.Form):
    title = forms.CharField(widget=forms.HiddenInput)
    content = forms.CharField(widget=forms.Textarea)





def editPage(request, title):


    if request.method == 'GET':
        print("Get")

        # Use this to retrieve the entry to display.  Put it in a function?
        entryContents = util.get_entry(title)
        form = EditPageForm(initial={'content': entryContents})
        print(form)


    # Trying to display the initial value of the form.

        if entryContents != None:

            findInstance = re.findall(title, entryContents, re.IGNORECASE)
            title = findInstance[0]

        else:
            return render(request, "encyclopedia/error.html", {
                "title": title
            })





        # return render(request, "encyclopedia/entry.html", {'form': form, "title": title, "entryContents": entryContents}
        #               )

        return render(request, "encyclopedia/entry.html", {'form': form, "title": title}
                      )

    # Need to handle request.post.
