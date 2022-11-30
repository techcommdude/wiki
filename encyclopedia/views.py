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


def newPage(request):

    # Check if method is POST
    if request.method == "GET":
        form = NewPageForm()

        return render(request, "encyclopedia/new.html", {'form': form}
                      )

    if request.method == "POST":
        # check if the form is valid and save the entry if it does not exist.
        return HttpResponse("Got a POST!")


def randomPage(request):
    # Random Page: Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.
    # Get the list of entries and randomly pick one and display it.
    form = RandomForm()
    return HttpResponse("Random Page!")


def displayPage(request, title):
    if request.method == 'GET':
        form = entryForm(initial={'content': page_html, 'title': title})


        return HttpResponse("Got a GET!")


def editPage(request, title):

    if request.method == 'GET':
        print("Got a Get!")

        # Use this to retrieve the entry to display.  Put it in a function?
        entryContents = util.get_entry(title)

        # This converts the Markdown to HTML and returns it.  Put it in a function?
        if entryContents != None:
            markdowner = Markdown()
            page_html = markdowner.convert(entryContents)

    # Trying to display the initial value of the form.

        if entryContents != None:

            # Finds the title in the entry with the correct case.
            findInstance = re.findall(title, entryContents, re.IGNORECASE)
            title = findInstance[0]

            # Initialize the form.
            form = EditPageForm(initial={'content': page_html, 'title': title})
            return render(request, "encyclopedia/edit.html", {'form': form, "title": title}
                          )

        else:
            return render(request, "encyclopedia/error.html", {
                "title": title
            })

    if request.method == 'POST':
        print("got a POST")
        return HttpResponse("Got a POST!")
