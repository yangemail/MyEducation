#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Yang Zhang
# site:

import xadmin

from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'created_time', 'last_modified_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', ]
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'created_time', 'last_modified_time']


class LessonAdmin(object):
    list_display = ['name', 'course', 'created_time', 'last_modified_time']
    search_fields = ['name', 'course', ]
    list_filter = ['name', 'course__name', 'created_time', 'last_modified_time']

class VideoAdmin(object):
    list_display = ['name','lesson', 'created_time', 'last_modified_time']
    search_fields = ['name','lesson', ]
    list_filter = ['name','lesson', 'created_time', 'last_modified_time']

class CourseResourceAdmin(object):
    list_display = ['name', 'download', 'course', 'created_time', 'last_modified_time']
    search_fields = ['name', 'download', 'course', ]
    list_filter = ['name', 'download', 'course', 'created_time', 'last_modified_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)