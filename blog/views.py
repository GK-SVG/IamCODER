from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import django.templatetags
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from urllib.parse import quote_plus
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core import serializers
import json
# Create your views here.

# blogCount = Blogpost.objects.all().count()

def home(request):
    # global_blog_count = 2
    t_blogs = Blogpost.objects.order_by('pub_date','view')[:10]
    blogs = Blogpost.objects.filter(public=True)
    params = {'blogs': blogs,"t_blogs":t_blogs}
    return render(request,'blog/home.html',params)


def load_more_blogs(request,global_blog_count):
    increase_blog_count = 2
    data = []
    if blogCount <= global_blog_count:
        blogs = Blogpost.objects.filter(public=True)[0:-(global_blog_count)]
        for blog in blogs:
            temp = {'img':f'{blog.IMG_url}','post_id':f'{blog.post_id}','user':f'{blog.user.username}','title':f'{blog.title}','pub_date':f'{blog.pub_date}','views':f'{blog.view}'}
            data.append(temp)
        return JsonResponse(data,safe=False)
    blogs = Blogpost.objects.filter(public=True)[-(global_blog_count+increase_blog_count):-(global_blog_count)]
    for blog in blogs:
        temp = {'img':f'{blog.IMG_url}','post_id':f'{blog.post_id}','user':f'{blog.user.username}','title':f'{blog.title}','pub_date':f'{blog.pub_date}','views':f'{blog.view}'}
        data.append(temp)
    return JsonResponse(data,safe=False)

def about(request):
    return render(request,'blog/about.html')

def blogpost(request,id):
    try:
        post = Blogpost.objects.get(post_id = id)
        share_string = quote_plus(post.title)
    except:
        messages.error(request,"Sommething Went wrong")
        return redirect("/")
    try:
        post_user_details = UserDetails.objects.get(user=post.user)
    except:
        post_user_details = []
    if request.user == post.user or post.public == True:
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
        try:
            f_user = FollowUser.objects.get(user=request.user,following=post.user)
            following = True
        except:
            following = False
        return render(request, 'blog/blogpost.html',{'post':post,'comment':comment, 'user':request.user , 'replyDict':replyDict,"share_string":share_string,"following":following,'post_user_details':post_user_details})
    else:
        messages.error(request,"Blog is private")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        # username charkters checker
        if not username.isalnum() :
             messages.error(request,'Your account not created Because')
             messages.error(request,'Username only contain alphaNumeric value')
             messages.error(request,'Please fill SIGN UP form again')
             return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))     

        # password1 and password2 checker     
        if password != password2 :
            messages.error(request,'Your account not created Because')
            messages.error(request,'Passwords do not match')
            messages.error(request,'Please fill SIGN UP form again')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        # creating user
        try:
            myuser=User.objects.get(username=username)
            messages.error(request,'The username you entered has already been taken. Please try another username.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        except:
            myuser = User.objects.create_user(username=username,email=email,password=password)
            myuser.first_name= fname
            myuser.last_name= lname
            myuser.save()
            user_details = UserDetails(user=myuser)
            user_details.save()
            login(request,myuser)
            request.session['user'] = myuser.username
            messages.success(request,'Your account created succesfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    else:
        return HttpResponse('404 - Not Found')

def handlelogin(request):
    if request.method == "POST":
        username = request.POST["loginusername"]
        password = request.POST["loginpassword"]
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            request.session['user'] = user.username
            messages.success(request,"Successfully Logged in")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponse('Error Not Found 404')

def handlelogout(request):
    logout(request)
    request.session.flush()
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
    blogs = Blogpost.objects.order_by('pub_date','view')[:20]
    params = {'blogs': blogs}
    return render(request,'blog/trending.html',params)



def post_blog(request):
    try:
        user = request.session['user']
        print("user==",user)
    except:
        messages.warning(request,"Please Login")
        return redirect("/")
    if user:
        if request.method=="POST":
            title = request.POST.get("title")
            img_url = request.POST.get("img_url")
            contant = request.POST.get("contant")
            print('request--',request.POST.get("public"))
            if request.POST.get("public") =='on':
                public = True
            else:
                print('request--',request.POST.get("public"))
                public = False
            user = request.user
            post = Blogpost(user=user,title=title,IMG_url=img_url,contant=contant,public=public)
            print('post--',post)
            post.save()
            print('post--',post)
            messages.success(request,"Post Created Successfully")
            return redirect("blogpost",post.post_id)
        return render(request,"blog/post_blog.html")
    messages.error(request,"Login For create New Blog")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    
def user_posts(request):
    try:
        user = request.session['user']
    except:
        messages.warning(request,"Please Login")
        return redirect("/")
    if user:
        user = request.user
        posts = Blogpost.objects.filter(user=user)
        return render(request,"blog/user_posts.html",{"blogs":posts})
    messages.error("Something went wrong")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_post(request,id):
    try:
        user = request.session['user']
        print("user==",user)
    except:
        messages.warning(request,"Please Login")
        return redirect("/")
    if user:
        try:
            post = Blogpost.objects.get(post_id=id)
            if request.user==post.user:
                post.delete()
                messages.success(request,"Post Deleted Successfully")
            else:
                messages.error(request,"You are not Authenticated for this action")
            return redirect("/")
        except:
            messages.error(request,"Post not available")
            return redirect("/")

def edit_post(request,id):
    print("request---",request.method,request.session['user'])
    try:
        user = request.session['user']
        # print("user==",user)
    except:
        messages.warning(request,"Please Login")
        return redirect("/")
    if request.method=="GET":
        try:
            post = Blogpost.objects.get(post_id=id)
            if request.user==post.user:
                print(post.title)
                return render(request,"blog/edit_post.html",{"post":post})
            else:
                messages.error(request,"You are not Authenticated for this action")
            return redirect("/")
        except:
            messages.error(request,"Post not available")
            return redirect("/")
    elif request.method=="POST":
        title = request.POST.get("title")
        img = request.POST.get("img_url")
        contant = request.POST.get("contant")
        print('public--',request.POST.get("public"))
        if request.POST.get("public") =='on':
            public = True
        else:
            public = False
        
        post = Blogpost.objects.get(post_id=id)
        if request.user==post.user:
            post.title = title
            post.IMG_url = img
            post.contant = contant
            post.public = public
            post.save()
            print(post.title)
            messages.success(request,"Post Edited Successfully")
            return redirect("blogpost",post.post_id)
        else:
            messages.error(request,"You are not Authenticated for this action")
        return redirect("/")
        

def Save_Blog(request,id):
    try:
        user = request.session['user']
    except:
        data = [{'message':"Please Login","status":'400','type':"warning"}]
        return JsonResponse(data,safe=False)
    try:
        blog = Blogpost.objects.get(post_id=id)
    except:
        data = [{'message':"Something went wrong","status":'404','type':"error"}]
        return JsonResponse(data,safe=False)
    savedBlog = SavedBlogs.objects.filter(user=request.user,blogs=blog).count()
    if savedBlog >=1:
        data = [{'message':"Blog Already Saved","status":'200','type':"warning"}]
        return JsonResponse(data,safe=False)
    else:
        saveBlog = SavedBlogs(user=request.user,blogs=blog)
        saveBlog.save()
        data = [{'message':"Blog Saved","status":'200','type':"success"}]
        return JsonResponse(data,safe=False)


def UserSavedBlogs(request):
    try:
        user = request.session['user']
    except:
        messages.error(request,"Please Login")
    AllSavedBlogs = SavedBlogs.objects.filter(user=request.user)
    return render(request,"blog/UserSavedBlogs.html",{'blogs':AllSavedBlogs})


def Follow_User(request,id):
    try:
        user = request.session['user']
    except:
        data = [{'message':"Please Login","status":'400','type':"warning"}]
        return JsonResponse(data,safe=False)
    try:
        f_user = User.objects.get(id=id)
    except:
        data = [{'message':"Something Wrong","status":'400','type':"error"}]
        return JsonResponse(data,safe=False)
    try:
        FollowUser.objects.get(user=request.user,following=f_user)
        data = [{'message':f"You already Following {f_user.username}","status":'200','type':"warning"}]
        return JsonResponse(data,safe=False)
    except:
        follow = FollowUser(user=request.user,following=f_user)
        follow.save()
        data = [{'message':f"Following {f_user.username}","status":'200','type':"success"}]
        return JsonResponse(data,safe=False)


def UnFollow_User(request,id):
    try:
        user = request.session['user']
    except:
        data = [{'message':"Please Login","status":'400','type':"warning"}]
        return JsonResponse(data,safe=False)
    try:
        f_user = User.objects.get(id=id)
    except:
        data = [{'message':"Something Wrong","status":'400','type':"error"}]
        return JsonResponse(data,safe=False)
    try:
        follow = FollowUser.objects.get(user=request.user,following=f_user)
    except:
        data = [{'message':"Something Went wronf","status":'404','type':"error"}]
        return JsonResponse(data,safe=False)
    follow.delete()
    data = [{'message':f"You Unfollowed {f_user.username}","status":'200','type':"warning"}]
    return JsonResponse(data,safe=False)


def user_profile(request,username):
    try:
        user = User.objects.get(username=username)
    except:
        messages.error(request,"User Does Not Exist")
        return redirect("/")
    try:
        f_user = FollowUser.objects.get(user=request.user,following=user)
        user_following = True
    except:
        user_following = False
    
    user_details = UserDetails.objects.get(user=user)
    blogs = Blogpost.objects.filter(user=user)
    blogs_count = Blogpost.objects.filter(user=user).count()
    followers = FollowUser.objects.filter(following=user)
    following = FollowUser.objects.filter(user=user)
    followers_count = FollowUser.objects.filter(following=user).count()
    following_count = FollowUser.objects.filter(user=user).count()
    # print("following--",following)
    # print("followers--",followers)
    savedBlogs_count = SavedBlogs.objects.filter(user=user).count()
    data = {'user':user,'user_details':user_details,'blogs':blogs,'followers':followers,'following':following,'followers_count':followers_count,'following_count':following_count,'savedBlogs_count':savedBlogs_count,'user_following':user_following,'blogs_count':blogs_count}
    return render(request,'blog/user_profile.html',data)
    

def edit_profile(request):
    if request.method=="POST":
        user_details = UserDetails.objects.get(user=request.user)
        if user_details:
            location = request.POST.get("location")
            education = request.POST.get("education")
            github = request.POST.get("github")
            work_at = request.POST.get("work_at")
            bio = request.POST.get("bio")
            user_details.location = location
            user_details.github_url = github
            user_details.education = education
            user_details.work_at = work_at
            user_details.descripation = bio
            user_details.save()
            messages.success(request,"Profile Details Edited Successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        messages.error(request,"User Not Exist")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    messages.error(request,"Something Went wrong")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



