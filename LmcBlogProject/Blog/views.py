from django.shortcuts import render,redirect,reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods,require_POST,require_GET
from .models import LMCBlogCategory,LMCBlog,LMCBlogComment
from .forms import LMCPubBlogForm
from django.http.response import JsonResponse
from django.db.models import Q

# Create your views here.
@login_required(login_url="auth/login")
def index(request):
  blogs = LMCBlog.objects.all()
  return render(request,'index.html',context={"blogs":blogs})

def blog_detail(request,blog_id):
  try:
    Blog = LMCBlog.objects.get(pk=blog_id)
  except Exception as e:
    Blog = None
  return render(request,'blog_detail.html',context={'Blog':Blog})

@require_http_methods(['GET','POST'])
@login_required(login_url="auth/login")
def pub_blog(request):
  if request.method == 'GET':
    categories = LMCBlogCategory.objects.all()
    return render(request,'pub_blog.html',context={"categories":categories})
  else:
    form = LMCPubBlogForm(request.POST)
    if form.is_valid():
      title = form.cleaned_data.get('title')
      content = form.cleaned_data.get('content')
      category_id = form.cleaned_data.get('category')
      blog = LMCBlog.objects.create(title=title,content=content,category_id=category_id,author=request.user)
      return JsonResponse({"code":200,"message":"Your blog has been successfully published.","data":{"blog_id":blog.id}})
    else:
      print(form.errors)
      return JsonResponse({'code':400,"message":"An error occurred! What bad luck..."})
    
@require_POST
@login_required()
def pub_comment(request):
  blog_id = request.POST.get('blog_id')
  content = request.POST.get('content')
  LMCBlogComment.objects.create(content=content,blog_id=blog_id,author=request.user)
  # 重新加载博客详情页
  return redirect(reverse("Blog:blog_detail",kwargs={'blog_id':blog_id}))

@require_GET
def search(request):
  # /search?q=xxx
  M = request.GET.get('M')
  # 从博客的标题和内容中查找含有M关键字的博客
  blogs = LMCBlog.objects.filter(Q(title__icontains = M) | Q(content__icontains = M)).all()
  return render(request,'index.html',context={"blogs":blogs})

