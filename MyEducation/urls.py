"""MyEducation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

import xadmin
from django.views.static import serve
from MyEducation.settings import MEDIA_ROOT

# from user.views import user_login
from organization.views import OrgView
from user.views import LoginView, RegisterView, UserActiveView, ForgetPasswordView, ResetView, ModifyPwdView, LogoutView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('captcha/', include('captcha.urls')),
    re_path(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),  # 显示media下面的图片

    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    # User Views
    # path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    re_path('^active/(?P<active_code>.*)/$', UserActiveView.as_view(), name='user_active'),
    path('forget/', ForgetPasswordView.as_view(), name='forget_pwd'),
    re_path('^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # 课程机构 url 配置
    # path('org_list/', OrgView.as_view(), name='org_list')
    path('org/', include(('organization.urls', 'organization'), namespace='org'))
]
