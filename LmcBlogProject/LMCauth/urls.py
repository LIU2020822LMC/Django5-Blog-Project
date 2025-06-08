from django.urls import path
from . import views

app_name = 'LMCauth'

urlpatterns = [
  path('login',views.LMClogin,name="login"),
  path('register',views.register,name="register"),
  path('captcha',views.LMC_send_email_captcha,name="email_captcha"),
  path('logout',views.LmcLogout,name="logout"),
]