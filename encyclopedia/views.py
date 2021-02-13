import re
from django.shortcuts import render
import markdown2

from . import util


def display_entry(request, entry_title):
    try:
        entry_title = request.GET['q']
    except:
        entry_title = entry_title
    entry_md = util.get_entry(entry_title)
    entry_html = markdown2.markdown(entry_md)
    return render(request, "encyclopedia/entry.html", {
        "entry_title": entry_title,
        "entry": entry_html})


def search(request):
    search_term = request.GET['q']
    existing_entries = util.list_entries()
    exact_match = [x for x in existing_entries if x.lower() ==
                   search_term.lower()]
    if exact_match:
        exact_match = exact_match[0]
    partial_matches = [
        x for x in existing_entries if search_term.lower() in x.lower()]

    if exact_match:
        return display_entry(request, exact_match)
    elif partial_matches:
        return render(request, "encyclopedia/partial_matches.html", {
            "partial_matches": partial_matches
        })
    else:
        return index(request)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
