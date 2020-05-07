from django.contrib import admin

# Register your models here.
from .models import Blogpost,BlogCommet
admin.site.register(BlogCommet)

@admin.register(Blogpost)
class BlogpostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyInject.js',)