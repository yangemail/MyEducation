#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Yang Zhang
# site:


from django.urls import path

from user.views import UpdateEmailView, MyCourseView
from user.views import UserInfoView, ImageUploadView, PasswordUpdateView, SendEmailCodeView
from user.views import MyFavOrgView, MyFavTeacher, MyFavCourseView, UserMessageView

urlpatterns = [
    # 用户信息
    path('info/', UserInfoView.as_view(), name='user_info'),  # 个人中心 - 首页
    path('image_upload/', ImageUploadView.as_view(), name='image_upload'),  # 个人中心 - 上传图片
    path('update/pwd/', PasswordUpdateView.as_view(), name='update_pwd'),  # 个人中心 - 修改密码功能
    path('sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),  # 发送邮箱验证码
    path('update_email/', UpdateEmailView.as_view(), name='update_email'), # 个人中心 - 修改邮箱
    path('mycourse/', MyCourseView.as_view(), name='mycourse'), # 个人中心 - 我的课程
    path('myfav/org/', MyFavOrgView.as_view(), name='myfav_org'), # 个人中心 - 我的收藏 - 机构
    path('myfav/teacher/', MyFavTeacher.as_view(), name='myfav_teacher'), # 个人中心 - 我的收藏 - 授课讲师
    path('myfav/course/', MyFavCourseView.as_view(), name='myfav_course'), # 个人中心 - 我的收藏 - 课程
    path('mymessage/', UserMessageView.as_view(), name='mymessage'), # 个人中心 - 我的消息

]
