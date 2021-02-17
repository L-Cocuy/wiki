import re
import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
import markdown2

from . import util

# TODO: Change forms to Django forms
# TODO: Use server-side validation of data submitted in form
# TODO: Add quotes around url calls in htmls


def new_entry(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new_entry.html")
    elif request.method == 'POST':
        entry_title = request.POST['q'].replace(" ", "_")
        if entry_title in util.list_entries():
            return render(request, "encyclopedia/storage_error.html")
        else:
            content = request.POST['markdown_content']
            util.save_entry(entry_title, content)
            return display_entry(request, entry_title)


def edit(request):
    if request.method == 'GET':
        entry_title = request.GET['entry_title']
        content = util.get_entry(entry_title)
        return render(request, "encyclopedia/edit.html", {
            "entry_title": entry_title,
            "content": content
        })

    elif request.method == 'POST':
        entry_title = request.POST['entry_title']
        content = request.POST['markdown_content']
        util.save_entry(entry_title, content)
        return display_entry(request, entry_title)


def delete_entry(request):
    entry_title = request.GET['entry_title']
    if util.delete_entry(entry_title):
        return index(request)
    else:
        return render(request, "encyclopedia/storage_error.html")


def random_page(request):
    entry_title = random.choice(util.list_entries())
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
