from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    contant = models.TextField(max_length=5000)
    pub_date = models.DateTimeField(auto_now_add=True)
    view = models.IntegerField(default=0)
    IMG_url = models.CharField(max_length=250,default='')

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


    