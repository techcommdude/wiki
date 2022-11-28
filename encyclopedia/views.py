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



    #Use this to retrieve the entry to display.  Put it in a function?
    test = util.get_entry(displayEntry)
    if test != None:
        print("Not in the wiki")

    a = (map(lambda x: x.lower(), entries))
    lower = list(a)
    print(lower)

    if displayEntry in lower:
        print("Entry is in the list")
        test = lower.index(displayEntry)
        print(test)
        print(entries[test])
        formatted = entries[test]

        entryContent = util.get_entry(displayEntry)

        return render(request, "encyclopedia/entry.html", {
            "displayEntry": formatted
        })
    else:

        return render(request, "encyclopedia/error.html", {
            "displayEntry": displayEntry
        })
