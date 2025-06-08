from django.shortcuts import render,redirect,reverse
from django.http.response import JsonResponse
import random
import string
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm,LoginForm
from django.contrib.auth import get_user_model,login,logout
from django.contrib.auth.models import User

User = get_user_model()


# Create your views here.

@csrf_protect  # 添加CSRF保护装饰器
@require_http_methods(['GET','POST'])
def LMClogin(request):
  if request.method == 'GET':
    return  render(request,"login.html")
  else:
    form = LoginForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data.get('email')
      password = form.cleaned_data.get('password')
      remember = form.cleaned_data.get('remember')
      user = User.objects.filter(email=email).first()
      if user and user.check_password(password):
        #登录
        login(request,user)

        #判断是否需要记住我
        if not remember:
          # 如果没有点击我，那么就要设置过期时间为0，即浏览器关闭后就会过期
          request.session.set_expiry(0)
        #如果点击了，那么就什么都不做，使用默认的2周的过期时间
        return redirect('/')
      else:
        print('邮箱或密码错误！')
        # form.add_error('email','邮箱或者密码错误！')
        # return render(request,'login.html',context={"form":form})
        return redirect(reverse('LMCauth:login'))


@csrf_protect  # 显式添加CSRF保护
@require_http_methods(["GET", "POST"])
def register(request):
  if request.method == 'GET':
    return render(request,"register.html")
  else:
   form = RegisterForm(request.POST)
   if form.is_valid():
     email = form.cleaned_data.get('email')
     username = form.cleaned_data.get('username')
     password = form.cleaned_data.get('password')
     User.objects.create_user(email=email,username=username,password=password)
     return redirect(reverse('LMCauth:login'))
   else:
     print(form.errors)
     #重新跳转到登录页面
     return render(request, "register.html", {'form': form})
   
def LmcLogout(request):
  logout(request)
  return redirect('/')

def LMC_send_email_captcha(request):
  #?email = xxx
  email = request.GET.get('email')
  if not email:
    return JsonResponse({"code":400,"message":"Must pass the mailbox!!!"})
  #生成验证码（取随机的6位阿拉伯数字）
  captcha = "".join(random.sample(string.digits,6))
  #存储到数据库当中
  CaptchaModel.objects.update_or_create(email=email,defaults={'captcha':captcha})
  send_mail("LMC博客注册验证码",message=f"您的注册验证码是：{captcha}",recipient_list=[email],from_email=None)
  return JsonResponse({"code":200,"message":"Email verification code sent successfully!"})

