import re
import random
from django.forms import widgets
from django.forms.fields import CharField
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django import forms
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def display_entry(request, entry_title):
    try:
        entry_title = request.GET['q']
    except:
        entry_title = entry_title
    entry_md = util.get_entry(entry_title)
    entry_html = markdown2.markdown(entry_md)
    return render(request, "encyclopedia/display_entry.html", {
        "entry_title": entry_title,
        "entry": entry_html})


def search(request):
    search_term = request.GET['q']
    existing_entries = util.list_entries()

    if exact_match := [x for x in existing_entries if x.lower() ==
                       search_term.lower()]:
        exact_match = exact_match[0]
        return display_entry(request, exact_match)

    elif partial_matches := [
            x for x in existing_entries if search_term.lower() in x.lower()]:
        return render(request, "encyclopedia/partial_matches.html", {
            "partial_matches": partial_matches,
            "search_term": search_term
        })

    else:
        # TODO: Add message to alert user his search did not return any results
        return index(request)


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
