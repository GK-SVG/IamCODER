from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='username')
    title = models.CharField(max_length=100)
    contant = models.TextField(max_length=5000)
    pub_date = models.DateTimeField(auto_now_add=True)
    view = models.IntegerField(default=0)
    IMG_url = models.CharField(max_length=250,default='')
    public = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title 


class BlogCommet(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment = models.TextField(max_length=250,default="")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Blogpost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,null=True)
    time = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:10] + "... by " + self.user.username 


class SavedBlogs(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    blogs = models.ForeignKey(Blogpost,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    

class FollowUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="fUser")

    def __str__(self):
        return self.user.username
    

class UserDetails(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    work_at = models.CharField(max_length=150,default="Team Computers Pvt. Ltd.")
    location = models.CharField(max_length=50,default="India, New Dehli")
    education = models.CharField(max_length=100,default="B.Tech in Computer Science and Engineering")
    descripation = models.CharField(max_length=150,default="Namaste 🙏🏼 I am Software Engineer at Team Computers")
    github_url  = models.URLField(default="https://github.com/")
    def __str__(self):
        return self.user.username
    