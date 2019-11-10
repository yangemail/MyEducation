#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Yang Zhang
# site:

import xadmin

from .models import UserAsk, CourseComment, UserFavorite, UserMessage, UserCourse


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'created_time']
    search_fields = ['name', 'mobile', 'course_name', ]
    list_filter = ['name', 'mobile', 'course_name', 'created_time']


class CourseCommentAdmin(object):
    list_display = ['user', 'course', 'comments', 'created_time', 'last_modified_time']
    search_fields = ['user', 'course', 'comments', ]
    list_filter = ['user', 'course', 'comments', 'created_time', 'last_modified_time']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'created_time', 'last_modified_time']
    search_fields = ['user', 'fav_id', 'fav_type', ]
    list_filter = ['user', 'fav_id', 'fav_type', 'created_time', 'last_modified_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'created_time', 'last_modified_time']
    search_fields = ['user', 'message', 'has_read', ]
    list_filter = ['user', 'message', 'has_read', 'created_time', 'last_modified_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'created_time']
    search_fields = ['user', 'course', 'created_time']
    list_filter = ['user', 'course', 'created_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
