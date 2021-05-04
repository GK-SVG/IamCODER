from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(BlogCommet)
admin.site.register(SavedBlogs)


@admin.register(Blogpost)
class BlogpostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyInject.js',)