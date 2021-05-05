"""IamCoder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from.import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path("post_blog/",views.post_blog,name="Post_Blog"),
    path('trending/',views.trending,name='trending'),
    path('blogpost/<int:id>',views.blogpost,name='blogpost'),
    path("search/", views.search, name="Search"), 
    path("signup/", views.signup, name="signup"), 
    path("login/", views.handlelogin, name="handlelogin"),
    path("logout/", views.handlelogout, name="handlelogout"),
    path("postComment/", views.postComment, name="postComment"),
    path("myPosts/",views.user_posts,name="UserPosts"),
    path("deletePost/<int:id>",views.delete_post,name="DeletePost"),
    path("editPost/<int:id>",views.edit_post,name="EditPost"),
    path("loadMore/<int:global_blog_count>",views.load_more_blogs,name="LoadMore"),
    path("saveBlog/<int:id>",views.Save_Blog,name="SaveBlog"),
    path("mySavedBlogs/",views.UserSavedBlogs,name="UserSavedBlogs"),
    path("followUser/<int:id>",views.Follow_User,name="Follow_User"),
    path("unfollowUser/<int:id>",views.UnFollow_User,name="UnFollow_User"),

]

