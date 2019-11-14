#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Yang Zhang
# site:
from django.urls import path

from .views import OrgListView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView

from .views import TeacherListView, TeacherDetailView

urlpatterns = [
    # 课程机构列表页
    path('list/', OrgListView.as_view(), name='org_list'),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
    # re_path('^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    path('home/<int:org_id>/', OrgHomeView.as_view(), name='org_home'),
    # re_path('^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    path('course/<int:org_id>/', OrgCourseView.as_view(), name='org_course'),
    # re_path('^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    path('desc/<int:org_id>/', OrgDescView.as_view(), name='org_desc'),
    # re_path('^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),
    path('org_teacher/<int:org_id>/', OrgTeacherView.as_view(), name='org_teacher'),

    # 机构收藏
    path('add_fav/', AddFavView.as_view(), name='add_fav'),

    # 讲师列表页
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),
    path('teacher/detail/<int:teacher_id>', TeacherDetailView.as_view(), name='teacher_detail')

]
