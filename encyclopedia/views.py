from django.shortcuts import render
import  random
from  django.urls import reverse
from  django.http import  HttpResponseRedirect
from  django import forms
from  django.contrib import messages
from  markdown2 import Markdown
from . import util


class SearchInput(forms.Form):
    title=forms.CharField(label='',widget=forms.TextInput(attrs={
            "class":"search",
            "placeholder":"Search Encyclopedia"
    }))
class CreateForm(forms.Form):
    title=forms.CharField(label='',widget=forms.TextInput(attrs={
            "class":"",
            "placeholder":"Title of new page"
    }))
    content=forms.CharField(label='',widget=forms.Textarea(attrs={"placeholder":"Add your content using GitHub Markdown",}))

class EditForm(forms.Form):
    content=forms.CharField(label='',widget=forms.Textarea(attrs={"placeholder":"Add your content using GitHub Markdown",}))

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "Search":SearchInput()
    })




def  entry(request,title):
    
    if util.get_entry(title) == None:
            return render(request, "encyclopedia/error.html", {
        "entry_title": title})   
    get_title= Markdown().convert(util.get_entry(title))

    return render(request, "encyclopedia/entries.html", {
        "entry_title": title,
        "entry_paragraph":get_title,    
        "Search":SearchInput()

    })   



def random_title(request):
    allEntries= util.list_entries()
    chosen=random.choice(allEntries)

    return HttpResponseRedirect(reverse("wiki",args=[chosen]))
    

def search(request):
    if request.method=="POST":
        form=SearchInput(request.POST)
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
            "Search":SearchInput()})

    

def create(request):
    if request.method == "POST":
        form=CreateForm(request.POST)
        if form.is_valid():
            cleanedForm=form.cleaned_data["title"]
            allEntries=[i.lower()for i in util.list_entries()]
            if cleanedForm.lower() in allEntries:

                messages.error(request,"This title is already exists")
                return render(request,"encyclopedia/create.html",{"create_from":form,"Search":SearchInput()})

            else:

                util.save_entry(form.cleaned_data['title'],form.cleaned_data['content'])
                return HttpResponseRedirect(reverse("wiki",args=[cleanedForm]))
      
    return render(request,"encyclopedia/create.html",{       
        "create_from":CreateForm(),    
        "Search":SearchInput()})


def edit(request,title):

    if request.method=="GET":
        dummy=Markdown().convert(util.get_entry(title))

        print(dummy)

        return render(request,"encyclopedia/edit.html",{   
            "title":title,    
            "edit_Form":EditForm(initial={'content':dummy}),    
            "Search":SearchInput()})   

    elif request.method=="POST":
        form=EditForm(request.POST)
        if form.is_valid():
            cleanedForm=form.cleaned_data["content"]
            if cleanedForm=='':
                messages.error(request,"This title is already exists")
                return render(request,"encyclopedia/edit.html",{"edit_Form":form,"Search":SearchInput()})
            else:
                util.save_entry(title,form.cleaned_data['content'])
                return HttpResponseRedirect(reverse("wiki",args=[title]))