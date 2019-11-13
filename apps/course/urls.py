#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Yang Zhang
# site:

from django.urls import path

from course.views import CourtListView, CourseDetailView, CourseInfoView

urlpatterns = [
    # 课程列表页
    path('list/', CourtListView.as_view(), name='course_list'),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    path('info/<int:course_id>/', CourseInfoView.as_view(), name='course_info'),
    path('comments/<int:course_id>/', CourseInfoView.as_view(), name='course_comments'),

]
