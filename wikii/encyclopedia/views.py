from django.shortcuts import render, redirect
from .util import save_entry, get_entry
from .forms import NewPageForm, SearchForm
from django.http import Http404
import random
import markdown2

from . import util

def index(request):
    search_form = SearchForm() 
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": search_form,  
    })

def new_page(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            if get_entry(title):
                form.add_error('title', 'An entry with this title already exists.')
            else:
                save_entry(title, content)
                return redirect('entry_page', title=title)
    else:
        form = NewPageForm()

    return render(request, 'encyclopedia/new_page.html', {'form': form})

def entry_page(request, title):
    content = get_entry(title)
    if content is None:
        raise Http404("Entry does not exist")
    
    html_content = markdown2.markdown(content)

    return render(request, 'encyclopedia/entry.html', {'title': title, 'content': content})

def random_page(request):
    entries = util.list_entries() 
    selected_page = random.choice(entries)
    return redirect('entry_page', title=selected_page)

def search_results(request):
    query = request.GET.get('query')
    entries = util.list_entries()
    results = []

    if query:
        if query in entries:
            return redirect('entry_page', title=query)

        for entry in entries:
            if query.lower() in entry.lower():
                results.append(entry)

    if len(results) == 1:
        return redirect('entry_page', title=results[0])
    elif results:
        return render(request, 'encyclopedia/search_results.html', {'query': query, 'results': results, 'search_form': SearchForm()})

    return redirect('search_results')



def edit_page(request, title):
    content = get_entry(title)
    if content is None:
        raise Http404("Entry does not exist")

    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data['title']
            new_content = form.cleaned_data['content']
            
            if new_title != title and get_entry(new_title):
                form.add_error('title', 'An entry with this title already exists.')
            else:
                save_entry(new_title, new_content)
                return redirect('entry_page', title=new_title)
    else:
        form = NewPageForm(initial={'title': title, 'content': content})
    
    return render(request, 'encyclopedia/edit_page.html', {'form': form, 'title': title})
