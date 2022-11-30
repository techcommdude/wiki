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

        return render(request, "encyclopedia/new.html", {'form': form})

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
        # form = entryForm()

        # this returns the proper title and the HTML to display on the displayPage
        htmlContent = returnHTML(title)
        titleDisplay = returnProperTitle(title)
        print(titleDisplay)
        print(htmlContent)

        if htmlContent != None:

            # return render(request, "encyclopedia/existing_entry.html", {'form': form, "testContent": testContent, "title": title}
            #                   )
            return render(request, "encyclopedia/existing_entry.html", {"htmlContent": htmlContent, "titleDisplay": titleDisplay}
                          )

        else:
            # Issue an HTML alert here instead.
            return render(request, "encyclopedia/error.html", {
                "title": title
            })


def returnHTML(title):

    entryContents = util.get_entry(title)
    if entryContents != None:

        markdowner = Markdown()
        page_html = markdowner.convert(entryContents)

        return page_html


def returnProperTitle(title):

    entryContents = util.get_entry(title)

    if entryContents != None:

        # Finds the title in the entry with the correct case.
        findInstance = re.findall(title, entryContents, re.IGNORECASE)
        newTitle = findInstance[0]

        return newTitle


def searchResults(request):
    if request.method == 'GET':

        return HttpResponse("On the search results page!")


def editPage(request, title):

    if request.method == 'POST':
        print("Got a Post!")

        # Use this to retrieve the entry to display.  Put it in a function?
        entryContents = util.get_entry(title)

    # Trying to display the initial value of the form.

        if entryContents != None:

            # Finds the title in the entry with the correct case.
            findInstance = re.findall(title, entryContents, re.IGNORECASE)
            title = findInstance[0]

            # Initialize the form.
            form = EditPageForm(
                initial={'content': entryContents, 'title': title})

            # render the page.
            return render(request, "encyclopedia/edit.html", {'form': form, "title": title}
                          )

    if request.method == 'Get':
        print("got a POST")
        return HttpResponse("Got a Get from the editPage view!")
