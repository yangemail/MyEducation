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
from django.urls import path, include, re_path
# from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from MyEducation.settings import MEDIA_ROOT #, STATIC_ROOT
from user.views import LoginView, RegisterView, UserActiveView, ForgetPasswordView, ResetView, ModifyPwdView, \
    LogoutView, IndexView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('captcha/', include('captcha.urls')),

    # 配置上传文件的访问处理函数
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),  # 显示media下面的图片
    # 显示static下面的图片(生产环境中，都由前端服务器调用静态文件，本配置只为本地测试使用)
    # re_path(r'^static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT }),

    # path('', TemplateView.as_view(template_name=''), name='index'),
    path('', IndexView.as_view(), name='index'),

    # User Views
    # path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    re_path('^active/(?P<active_code>.*)/$', UserActiveView.as_view(), name='user_active'),
    path('forget/', ForgetPasswordView.as_view(), name='forget_pwd'),
    re_path('^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),

    # 富文本相关url
    path('ueditor/', include('DjangoUeditor.urls')),

    # 机构 url 配置
    # path('org_list/', OrgView.as_view(), name='org_list')
    path('org/', include(('organization.urls', 'organization'), namespace='org')),

    # 讲师 url 配置
    # path('org/', include(('organization.urls', 'organization'), namespace='teacher')),

    # 课程 url 配置
    path('course/', include(('course.urls', 'course'), namespace='course')),

    # 用户
    path('users/', include(('user.urls', 'users'), namespace='users')),

    # Blog
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
]

# 全局404页面配置
handler404 = 'user.views.page_not_found'
handler500 = 'user.views.page_error'
