#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Yang Zhang
# site:

import xadmin

from .models import City, CourseOrganization, Teacher


class CityAdmin(object):
    list_display = ['name', 'desc', 'created_time', 'last_modified_time']
    search_fields = ['name', 'desc', ]
    list_filter = ['name', 'desc', 'created_time', 'last_modified_time']


class CourseOrganizationAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'created_time',
                    'last_modified_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', ]
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'created_time',
                   'last_modified_time']
    # relfield_style = 'fk-ajax' # 以Ajax加载的方式完成显示（对于指向此model的外键）


class TeacherAdmin(object):
    list_display = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
                    'courseorganization', 'created_time', 'last_modified_time']
    search_fields = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
                     'courseorganization', ]
    list_filter = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
                   'courseorganization', 'created_time', 'last_modified_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrganization, CourseOrganizationAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
