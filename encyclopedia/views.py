from django.http import HttpResponse
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def displayEntry(request, entry):

    entries = []
    entries = util.list_entries()
    print(entries)

    a = (map(lambda x: x.lower(), entries))
    lower = list(a)
    print(lower)

    if entry in lower:
        print("Entry is in the list")
        test = lower.index(entry)
        print(test)
        print(entries[test])
        formatted = entries[test]

        entryContent = util.get_entry(entry)

        return render(request, "encyclopedia/entry.html", {
            "entry": formatted
        })
    else:
        # return HttpResponse(f"Error, " + entry + " is not in the wiki!"

        return render(request, "encyclopedia/error.html", {
            "entry": entry
        })
