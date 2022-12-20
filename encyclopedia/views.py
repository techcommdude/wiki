import random
import re
from django.forms import formset_factory
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


class NewPageForm(forms.Form):
    new_title = forms.CharField(label='Topic title:')
    new_content = forms.CharField(
        widget=forms.Textarea, label='Topic content:')


class EditPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(
        attrs={'readonly': 'readonly'}))
    content = forms.CharField(widget=forms.Textarea, label='')


def newPage(request):

    if request.method == "GET":
        form = NewPageForm()

        return render(request, "encyclopedia/new.html", {'form': form})

    if request.method == "POST":

        form = NewPageForm(request.POST)
        print(form.as_p())
        print("End of errors!")
        if form.is_valid():
            new_content = form.cleaned_data['new_content']
            new_title = form.cleaned_data['new_title']

            if util.get_entry(new_title) == None:

                print(new_content)
                new_content = "# " + new_title + " \n" + new_content
                new_content = new_content.replace('\r', '')
                print(new_title)
                print(new_content)

                util.save_entry(new_title, new_content)
                print("The content has been saved!")
                return HttpResponseRedirect(reverse("entries:index"))
            else:
                 # This is an alert for an error.
                return render(request, "encyclopedia/error_exists.html", {"existing": True, "new_title": new_title})


def randomPage(request):
    # Random Page: Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.
    # Get the list of entries and randomly pick one and display it.
    if request.method == 'GET':
        titles = util.list_entries()
        randomPick = random.choice(titles)
        htmlContent = returnHTML(randomPick)
        titleDisplay = returnProperTitle(randomPick)
        print(titleDisplay)
        print(htmlContent)

    if htmlContent != None:

        return render(request, "encyclopedia/existing_entry.html", {"htmlContent": htmlContent, "titleDisplay": titleDisplay}
                      )


def displayPage(request, title):
    if request.method == 'GET':

        # this returns the proper title and the HTML to display on the displayPage
        htmlContent = returnHTML(title)
        titleDisplay = returnProperTitle(title)
        print(titleDisplay)
        print(htmlContent)

        if htmlContent != None:

            return render(request, "encyclopedia/existing_entry.html", {"htmlContent": htmlContent, "titleDisplay": titleDisplay}
                          )

        else:
            # Issue an HTML alert here
            return render(request, "encyclopedia/error.html", {
                "title": title, "exists": False
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

        # Do a substring search for queryResult
        searchList = util.list_entries()
        lowerSearchList = [item.lower() for item in searchList]
        print(lowerSearchList)

        # This works for the general search of existing topics.
        indices = [i for i, x in enumerate(lowerSearchList) if x == title]
        print(indices)

        # Finds the title in the entry with the correct case.
        findInstance = re.findall(title, entryContents, re.IGNORECASE)
        newTitle = findInstance[0]

        return newTitle


def searchResults(request):

    if request.method == 'GET':
        queryResult = request.GET
        query = queryResult['q']

        # Do a substring search for queryResult
        searchList = util.list_entries()





        lowerSearchList = [item.lower() for item in searchList]
        print(lowerSearchList)

       #If query is in searchList, then go to the page directly at this point.
        # otherwise continue.
        if query.lower() in lowerSearchList:

            titleDisplay = query.lower()
            htmlContent = returnHTML(query)
            # render the page since the search was an exact match.
            return render(request, "encyclopedia/existing_entry.html", {"htmlContent": htmlContent, "titleDisplay": titleDisplay}
                          )


        # Yahoo this works! for the substring search.
        indices = []
        for i, elem in enumerate(lowerSearchList):
            if query in elem:
                if query.lower() in lowerSearchList:
                    print("Do nothing")
                else:
                    indices.append(i)
        print(indices)

        #TODO: If the entry exists, go directly to that entry.  If you only get substring
        # results, then print it to screen.

        substringSearchResults = []
        for i in indices:
            substringSearchResults.append(searchList[i])
        print(substringSearchResults)

        if len(substringSearchResults) == 0:
            # return HttpResponse("No search results.")

            # Issue an HTML alert here
            return render(request, "encyclopedia/error.html", {
                "query": query, "noResults": False
            })

        else:

            return render(request, "encyclopedia/searchresults.html", {
            "results": substringSearchResults
        })


def editPage(request, title):

    if request.method == 'GET':

        # this may not be required.
        print("got a GET")

        entryContents = util.get_entry(title)

        # Trying to display the initial value of the form.
        if entryContents != None:

            # Finds the title in the entry with the correct case.
            findInstance = re.findall(title, entryContents, re.IGNORECASE)
            title = findInstance[0]

        # Use this to retrieve the entry to display.  Put it in a function?
        # entryContents = util.get_entry(title)
        stripString = "# " + title + "\n\n"
        print(stripString)

        # prepare the body for inserting into the edit page.
        titleToInsert = "# " + title
        # Strips the leading spaces.
        entryContents.strip()
        print(entryContents)
        t = entryContents.removeprefix(titleToInsert)
        # Left strip characters.
        finalContentsInsert = t.lstrip()

        # Initialize the form with entry text that is stripped of extra characters.
        form = EditPageForm(
            initial={'content': finalContentsInsert, 'title': title})

        # render the page.
        return render(request, "encyclopedia/edit.html", {'form': form, "title": title}
                      )

    if request.method == 'POST':

        form = EditPageForm(request.POST)
        print(form.as_p())
        print("End of errors!")
        if form.is_valid():
            content = form.cleaned_data['content']
            title = form.cleaned_data['title']
            print(content)
            content = "# " + title + " \n" + content
            content = content.replace('\r', '')
            print(title)
            print(content)

            # Need to strip out the

            util.save_entry(title, content)
            print("The content has been saved!")
            return HttpResponseRedirect(reverse("entries:index"))

            # return HttpResponse("The content has been saved!")

        else:
            # re-render invalid form with same information.
            return render(request, "encyclopedia/edit.html", {'form': form, "title": title}
                          )
