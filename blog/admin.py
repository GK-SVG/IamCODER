from django.contrib import admin

# Register your models here.
from .models import Blogpost,BlogCommet
admin.site.register(Blogpost)
admin.site.register(BlogCommet)