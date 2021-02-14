import re
from django.shortcuts import render
import markdown2

from . import util


def new_entry(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new_entry.html")
    elif request.method == 'POST':
        entry_title = request.POST['q']
        content = request.POST['markdown_content']
        util.save_entry(entry_title, content)
        return display_entry(request, entry_title)


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
            "partial_matches": partial_matches,
            "search_term": search_term
        })
    else:
        # TODO: Add message to alert user his search did not return any results
        return index(request)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
