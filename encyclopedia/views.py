import random
import re
from django.contrib import messages
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
        print("End of errors!")
        if form.is_valid():
            new_content = form.cleaned_data['new_content']
            new_title = form.cleaned_data['new_title']

            if util.get_entry(new_title) == None:

                new_content = "# " + new_title + " \n" + new_content
                new_content = new_content.replace('\r', '')

                util.save_entry(new_title, new_content)
                print("The content has been saved!")

                htmlContent = returnHTML(new_title)
                titleDisplay = returnProperTitle(new_title)

                # Display the new page here after it is created.
                messages.success(request, 'New page has been created.')
                return render(request, "encyclopedia/existing_entry.html", {"htmlContent": htmlContent, "titleDisplay": titleDisplay}
                              )
            else:
                # This is an alert for an error.
                messages.error(request, 'This topic already exists in the wiki. Please try again.')
                return render(request, "encyclopedia/error_exists.html", {"existing": True, "new_title": new_title})


def randomPage(request):
    # Random Page: Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.
    # Get the list of entries and randomly pick one and display it.
    if request.method == 'GET':
        titles = util.list_entries()
        randomPick = random.choice(titles)
        htmlContent = returnHTML(randomPick)
        titleDisplay = returnProperTitle(randomPick)

    if htmlContent != None:

                  # Issue an HTML alert here
        messages.success(request, 'Random page displayed.')
        return render(request, "encyclopedia/existing_entry.html", {"htmlContent": htmlContent, "titleDisplay": titleDisplay}
                      )


def displayPage(request, title):
    if request.method == 'GET':

        # this returns the proper title and the HTML to display on the displayPage
        htmlContent = returnHTML(title)
        titleDisplay = returnProperTitle(title)

        if htmlContent != None:

            # Render the then entry after you create it.
            return render(request, "encyclopedia/existing_entry.html", {"htmlContent": htmlContent, "titleDisplay": titleDisplay}
                          )

        else:
            # Issue an HTML alert here
            messages.error(request, 'No entries found for your search.')
            return HttpResponseRedirect(reverse("entries:index"))


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

        # This works for the general search of existing topics.
        indices = [i for i, x in enumerate(lowerSearchList) if x == title]

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

       # If query is in searchList, then go to the page directly at this point.
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

        # If the entry exists, go directly to that entry.  If you only get substring
        # results, then print it to screen.

        substringSearchResults = []
        for i in indices:
            substringSearchResults.append(searchList[i])

        if len(substringSearchResults) == 0:
            # No search results, so return an error.
            messages.error(request, 'No entries found for your search.')
            return HttpResponseRedirect(reverse("entries:index"))

        else:

            return render(request, "encyclopedia/searchresults.html", {
                "results": substringSearchResults
            })


def editPage(request, title):

    if request.method == 'GET':

        entryContents = util.get_entry(title)

        # Trying to display the initial value of the form.
        if entryContents != None:

            # Finds the title in the entry with the correct case.
            findInstance = re.findall(title, entryContents, re.IGNORECASE)
            title = findInstance[0]

        # Use this to retrieve the entry to display.  Put it in a function?
        stripString = "# " + title + "\n\n"

        # prepare the body for inserting into the edit page.
        titleToInsert = "# " + title
        # Strips the leading spaces.
        entryContents.strip()
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
        print("End of errors!")
        if form.is_valid():
            content = form.cleaned_data['content']
            title = form.cleaned_data['title']

            content = "# " + title + " \n" + content
            content = content.replace('\r', '')

            # Display the form again or at least display a message.
            util.save_entry(title, content)

            # this returns the proper title and the HTML to display on the displayPage
            htmlContent = returnHTML(title)
            titleDisplay = returnProperTitle(title)

            print("The content has been saved!")
            # Display the page again.

            # Issue an HTML alert here
            messages.info(request, 'Your entry has been saved.')
            return render(request, "encyclopedia/existing_entry.html", {"htmlContent": htmlContent, "titleDisplay": titleDisplay}
                          )

        # return HttpResponse("The content has been saved!")

        else:
            # re-render invalid form with same information.
            return render(request, "encyclopedia/edit.html", {'form': form, "title": title}
                          )


def handler404(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response
