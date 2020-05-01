from django.db import models

# Create your models here.
class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    writter = models.CharField(max_length=50,default="")
    title = models.CharField(max_length=100)
    desc = models.TextField(max_length=500,default="")
    contant = models.TextField(max_length=5000)
    pub_date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='blog/images', default="")

    def __str__(self):
        return self.title 