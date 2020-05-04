from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from.models import Blogpost
from django.contrib.auth.models import User
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


def search(request):
    query = request.GET.get('query')
    if len(query)>80:
        blogs = []
    else:
        blogTitle = Blogpost.objects.filter(title__icontains=query)
        blogContant = Blogpost.objects.filter(contant__icontains=query)
        blogs = blogTitle.union(blogContant)
    if blogs.count==0:
        messages.warning(request,"No search Found please refine your search ")
    return render(request,'blog/search.html',{'blogs':blogs, 'query': query})


def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email=request.POST['email']
        password=request.POST['pass1']
        password2=request.POST['pass2']
        # CHECKPOINTS
    if len(username) > 12 :
        messages.error(request,'Your account not created Because')
        messages.error(request,'Username must have maximum 12 Charcters')
        messages.error(request,'Please fill SIGN UP form again')
        return redirect('/')
    if not username.isalnum() :
        messages.error(request,'Your account not created Because')
        messages.error(request,'Username only contain alphaNumeric value')
        messages.error(request,'Please fill SIGN UP form again')
        return redirect('/')
    if password != password2 :
        messages.error(request,'Your account not created Because')
        messages.error(request,'Passwords do not match')
        messages.error(request,'Please fill SIGN UP form again')
        return redirect('/')

        # creating user
        myuser = User.objects.create_user(username=username,email=email,password=password)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request,'Your account created succesfully')
        return redirect('/')
    else:
        return HttpResponse('404 - Not Found')