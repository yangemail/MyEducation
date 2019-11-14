#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Yang Zhang
# site:


from django.urls import path
from django.views.generic import TemplateView

from user.views import UserInfoView, UserUserMessageView, ImageUploadView, PasswordUpdateView, SendEmailCodeView

urlpatterns = [
    # 用户信息
    path('info/', UserInfoView.as_view(), name='user_info'),  # 个人中心 - 首页
    path('image_upload/', ImageUploadView.as_view(), name='image_upload'),  # 个人中心 - 上传图片
    path('update/pwd/', PasswordUpdateView.as_view(), name='update_pwd'),  # 个人中心 - 修改密码功能
    path('sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),  # 发送邮箱验证码
    path('update_email/', None, name='update_email'),

    path('mymessage/', UserUserMessageView.as_view(), name='mymessage'),
    path('mycourse/', TemplateView.as_view(template_name=''), name='mycourse'),
    path('myfav_org/', TemplateView.as_view(template_name=''), name='myfav_org'),

]
