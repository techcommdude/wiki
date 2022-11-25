from django.http import HttpResponse
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def displayEntry(request, entry):

    # if util.get_entry(entry):
    #     entryContent = entry
    #     return render(request, "encyclopedia/entry.html", {
    #         "entry": entry.capitalize()
    #     })
    # else:
    #     return HttpResponse(f"Error, " + entry + " is not in the wiki!")

    entries = []
    entries = util.list_entries()
    print(entries)


    a = (map(lambda x: x.lower(), entries))
    lower = list(a)
    print(lower)




    # for entry in entries:
    #     print(entry)

    # if entry.capitalize() in entries:
    # print(entry)
    # test = entries.index(entry)
    # test2 = str(test)
    # print(test2)

    if util.get_entry(entry):
        # test = entries.index(entry)
        entryContent = util.get_entry(entry)

        # index = entries.index(entry)
        # print(index)

        return render(request, "encyclopedia/entry.html", {
            "entry": entry
        })
    else:
        return HttpResponse(f"Error, " + entry + " is not in the wiki!")
