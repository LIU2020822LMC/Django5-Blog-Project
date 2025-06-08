from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class LMCBlogCategory(models.Model):
  name = models.CharField(max_length=200,verbose_name='分类名称')

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = '博客分类'
    verbose_name_plural = verbose_name

class LMCBlog(models.Model):
  title = models.CharField(max_length=200,verbose_name='标题')
  content = models.TextField(verbose_name='博客内容')
  pub_time = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
  category = models.ForeignKey(LMCBlogCategory,on_delete=models.CASCADE,verbose_name='博客分类')
  author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')

  def __str__(self):
    return self.title

  class Meta:
    verbose_name = '博客'
    verbose_name_plural = verbose_name
    ordering = ['-pub_time'] #根据发布时间倒序排序，也就是按照新发布的排第一



class LMCBlogComment(models.Model):
  content = models.TextField(verbose_name='博客内容')
  pub_time = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
  blog = models.ForeignKey(LMCBlog,on_delete=models.CASCADE,related_name="comments",verbose_name='所属博客')
  author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')

  def __str__(self):
    return self.content

  class Meta:
    verbose_name = '评论'
    verbose_name_plural = verbose_name
    ordering = ['-pub_time'] #根据发布时间倒序排序