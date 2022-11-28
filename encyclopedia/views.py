import re
from django.http import HttpResponse
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def displayEntry(request, displayEntry):

    entries = []
    entries = util.list_entries()
    print(entries)

    # matches = []
    # for match in entries:
    #     if displayEntry in match:
    #         matches.append(match)

    # print(matches)



    #Use this to retrieve the entry to display.  Put it in a function?
    entryContents = util.get_entry(displayEntry)

    # x = re.findall("[a-s]", entryContents, re.IGNORECASE)
    # print(x)

    # x = re.search(displayEntry, entryContents, re.IGNORECASE)
    # print(x)

    #if entryContents returns None, do not do this search since it leads to error.

    if entryContents != None:

        x = re.findall(displayEntry, entryContents, re.IGNORECASE)

        #If the list returned is not empty, print the first one.
        print(x[0])

        return render(request, "encyclopedia/entry.html", {
            "displayEntry": x[0]
        })


    else:
        return render(request, "encyclopedia/error.html", {
        "displayEntry": displayEntry
        })
