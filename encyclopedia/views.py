from django.shortcuts import render
import  random
from  django.urls import reverse
from  django.http import  HttpResponseRedirect
from  django import forms
from  django.contrib import messages
from  markdown2 import Markdown
from . import util


class SearchInputForm(forms.Form):
    title=forms.CharField(label='',widget=forms.TextInput(attrs={
            "class":"search",
            "placeholder":"Search Encyclopedia"
    }))

class InputForm(forms.Form):
    title=forms.CharField(label='',widget=forms.TextInput(attrs={
            "class":"",
            "placeholder":"Add yout Title"
    }))

class TextArea(forms.Form):
    content=forms.CharField(label='',widget=forms.Textarea(attrs={"placeholder":"Add your content using GitHub Markdown",}))


def index(request):
    '''
    Index Page: 
    Update index.html such that, instead of merely listing the names of all pages in the encyclopedia, 
    user can click on any entry name to be taken directly to that entry page.
    '''

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "Search":SearchInputForm()
    })

def  entry(request,title):
    '''
    Entry Page:
    Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, 
    should render a page that displays the contents of that encyclopedia entry.

    1.The view should get the content of the encyclopedia entry by calling the appropriate util function.

    2.If an entry is requested that does not exist, 
      the user should be presented with an error page indicating that their requested page was not found.

    3.If the entry does exist, the user should be presented with a page that displays the content of the entry.
      The title of the page should include the name of the entry.
    '''
    
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html", {
        "entry_title": title})   

    get_title= Markdown().convert(util.get_entry(title))
    return render(request, "encyclopedia/entries.html", {
        "entry_title": title,
        "entry_paragraph":get_title,    
        "Search":SearchInputForm(),

    })   

def random_title(request):
    '''
    Random Page: 
    Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.
    '''

    allEntries= util.list_entries()
    chosen=random.choice(allEntries)
    return HttpResponseRedirect(reverse("wiki",args=[chosen]))
    

def search(request):
    '''
    Search: 
    Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry.

    1.If the query matches the name of an encyclopedia entry, 
      the user should be redirected to that entry’s page.
    
    2.If the query does not match the name of an encyclopedia entry, 
      the user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring.
      For example, if the search query were ytho, then Python should appear in the search results.
    
    3.Clicking on any of the entry names on the search results page should take the user to that entry’s page.
    '''

    if request.method=="POST":
        form=InputForm(request.POST)
        if form.is_valid():
            cleanedForm=form.cleaned_data['title'].lower()
            allEntries=[i.lower()for i in util.list_entries()]

            if cleanedForm in allEntries:
                indexs=allEntries.index(cleanedForm)
                return HttpResponseRedirect(reverse("wiki",args=[util.list_entries()[indexs]]))
            else:
                data=[ i for i in util.list_entries() if cleanedForm in i.lower() ]
                print(data)
                return render(request, "encyclopedia/search.html", {
            "entries": data,
            "Search":SearchInputForm()})

    

def create(request):
    '''
    New Page:
    Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry.

    1.Users should be able to enter a title for the page and,
     in a textarea, should be able to enter the Markdown content for the page.

    2.Users should be able to click a button to save their new page.

    3.When the page is saved, 
     if an encyclopedia entry already exists with the provided title,
     the user should be presented with an error message.

    4.Otherwise, the encyclopedia entry should be saved to disk,
      and the user should be taken to the new entry’s page.
    '''

    if request.method == "POST":
        form= [TextArea(request.POST),InputForm(request.POST)]
        
        if form[0].is_valid() and form[1].is_valid() :

            cleanedForm=form[1].cleaned_data["title"]
            allEntries=[i.lower() for i in util.list_entries()]
            if cleanedForm.lower() in allEntries:
                messages.error(request,f"This title is already exists : {cleanedForm}")
                return render(request,"encyclopedia/create.html",
                {
                "create_form":form[0],
                "title_form":form[1],
                "Search":SearchInputForm(),
                })

            else:
                util.save_entry(form.cleaned_data['title'],form.cleaned_data['content'])
                return HttpResponseRedirect(reverse("wiki",args=[cleanedForm]))
      
    return render(request,"encyclopedia/create.html",{       
        "create_form":TextArea(),
        "title_form":InputForm(),    
        "Search":SearchInputForm()})


def edit(request,title):
    '''
    Edit Page:
    On each entry page, 
    the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.

    1.The textarea should be pre-populated with the existing Markdown content of the page. 
      (i.e., the existing content should be the initial value of the textarea).

    2.The user should be able to click a button to save the changes made to the entry.

    3.Once the entry is saved, 
      the user should be redirected back to that entry’s page.
    '''

    if request.method=="GET":

        text=Markdown().convert(util.get_entry(title))
        return render(request,"encyclopedia/edit.html",{   
            "title":title,    
            "edit_form":TextArea(initial={'content':text}),    
            "Search":SearchInputForm()})   

    elif request.method=="POST":
        form=TextArea(request.POST)
        if form.is_valid():
            util.save_entry(title,form.cleaned_data['content'])
            return HttpResponseRedirect(reverse("wiki",args=[title]))