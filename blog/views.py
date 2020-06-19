from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from.models import Blogpost, BlogCommet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import django.templatetags
from django.utils import timezone
# Create your views here.

def home(request):
    blogs = Blogpost.objects.all()
    params = {'blogs': blogs}
    return render(request,'blog/home.html',params)

def about(request):
    return render(request,'blog/about.html')

def blogpost(request,id):
    latests=Blogpost.objects.order_by('-pub_date')[:3]
    post = Blogpost.objects.filter(post_id = id)[0]
    post.view= post.view+1
    post.save()
    comment = BlogCommet.objects.filter(post=post,parent=None)
    replies = BlogCommet.objects.filter(post=post).exclude(parent=None) 
    replyDict = {}
    for reply in replies:
        if reply.parent.comment_id not in replyDict.keys():
            replyDict[reply.parent.comment_id]=[reply]
        else:
            replyDict[reply.parent.comment_id].append(reply)
    return render(request, 'blog/blogpost.html',{'post':post,'comment':comment, 'user':request.user , 'replyDict':replyDict,'latests':latests})


def search(request):
    query = request.GET.get('query')
    if len(query)==0:
        return redirect('/')
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

        # checkpoints 
        #username length checker
        if len(username) > 12 :
            messages.error(request,'Your account not created Because')
            messages.error(request,'Username must have maximum 12 Charcters')
            messages.error(request,'Please fill SIGN UP form again')
            return redirect('/')

        # username charkters checker
        if not username.isalnum() :
             messages.error(request,'Your account not created Because')
             messages.error(request,'Username only contain alphaNumeric value')
             messages.error(request,'Please fill SIGN UP form again')
             return redirect('/')       

        # password1 and password2 checker     
        if password != password2 :
            messages.error(request,'Your account not created Because')
            messages.error(request,'Passwords do not match')
            messages.error(request,'Please fill SIGN UP form again')
            return redirect('/')
        # creating user
        try:
            myuser=User.objects.get(username=username)
            messages.error(request,'The username you entered has already been taken. Please try another username.')
            return redirect('/')
        except:
            myuser = User.objects.create_user(username=username,email=email,password=password)
            myuser.first_name= fname
            myuser.last_name= lname
            myuser.save()
            messages.success(request,'Your account created succesfully')
            return redirect('/')
        
    else:
        return HttpResponse('404 - Not Found')

def handlelogin(request):
    if request.method == "POST":
        username = request.POST["loginusername"]
        password = request.POST["loginpassword"]
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged in")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect('/')
    else:
        return HttpResponse('Error Not Found 404')

def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('/')

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postId = request.POST.get("post_id") 
        post = Blogpost.objects.get(post_id=postId)
        parentId = request.POST.get("reply_id")        
        if parentId == "": 
            if len(comment) > 0:
                comment = BlogCommet(comment=comment,user=user,post=post)
                comment.save()
                messages.success(request,"Comment posted successfully")
            else:
                messages.warning(request,"Comment block never blank Please write something")  
        else:
            parent = BlogCommet.objects.get(comment_id=parentId)
            comment = BlogCommet(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request,"Reply posted successfully")
        
              
    return redirect(f"/blogpost/{post.post_id}")

def trending(request):
    blogs = Blogpost.objects.order_by('-pub_date','view')[:10]
    params = {'blogs': blogs}
    return render(request,'blog/trending.html',params)
