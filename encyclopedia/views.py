from django.shortcuts import render
import markdown2

from . import util


def display_entry(request, entry_title):
    entry_md = util.get_entry(entry_title)
    entry_html = markdown2.markdown(entry_md)
    return render(request, "encyclopedia/entry.html", {
        "entry_title": entry_title,
        "entry": entry_html})


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
