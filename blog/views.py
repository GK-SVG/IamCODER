from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from.models import Blogpost
# Create your views here.

def home(request):
    blogs = Blogpost.objects.all()
    params = {'blogs': blogs}
    return render(request,'blog/home.html',params)

def about(request):
    return render(request,'blog/about.html')

def blogpost(request,id):
    post = Blogpost.objects.filter(post_id = id)[0]
    return render(request, 'blog/blogpost.html',{'post':post})
