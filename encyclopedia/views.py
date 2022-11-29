import re
from markdown2 import Markdown
from django import forms
from django.http import HttpResponse
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

class entryForm(forms.Form):
    title = forms.CharField(label='')
    existingEntry = forms.CharField(widget=forms.Textarea)

class RandomForm(forms.Form):
    title = forms.CharField(label='')
    content = forms.CharField(widget=forms.Textarea)

class NewPageForm(forms.Form):
    new_title = forms.CharField(label='')
    new_content = forms.CharField(widget=forms.Textarea, label='')

class EditPageForm(forms.Form):
    # title = forms.CharField(widget=forms.HiddenInput)
    title = forms.CharField(label='')
    content = forms.CharField(widget=forms.Textarea, label='')


def newPage (request):
    form = NewPageForm()
    # return HttpResponse("New Page!")
    return render(request, "encyclopedia/new.html", {'form': form}
                      )


def randomPage (request):
    form = RandomForm()
    return HttpResponse("Random Page!")



def editPage(request, title):

    if request.method == 'GET':
        print("Got a Get!")

        # Use this to retrieve the entry to display.  Put it in a function?
        entryContents = util.get_entry(title)

        #Need to return the HTML here.
        if entryContents != None:
            markdowner = Markdown()
            page_html = markdowner.convert(entryContents)


            form = EditPageForm(initial={'content': page_html, 'title': title})
            print(form)


    # Trying to display the initial value of the form.

        if entryContents != None:

            findInstance = re.findall(title, entryContents, re.IGNORECASE)
            title = findInstance[0]
            form = EditPageForm(initial={'content': page_html, 'title': title})
            return render(request, "encyclopedia/entry.html", {'form': form, "title": title}
                      )

        else:
            return render(request, "encyclopedia/error.html", {
                "title": title
            })

    if request.method == 'POST':
        print("got a POST")
        return HttpResponse("Got a POST!")
