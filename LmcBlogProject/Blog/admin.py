from django.contrib import admin
from .models import *

# Register your models here.
class LMCBlogCategoryAdmin(admin.ModelAdmin):
  list_display = ['name']


class LMCBlogAdmin(admin.ModelAdmin):
  list_display = ['title','content','pub_time','category','author']


class LMCBlogCommentAdmin(admin.ModelAdmin):
  list_display = ['content','pub_time','author','blog']


admin.site.register(LMCBlogCategory,LMCBlogCategoryAdmin)
admin.site.register(LMCBlog,LMCBlogAdmin)
admin.site.register(LMCBlogComment,LMCBlogCommentAdmin)