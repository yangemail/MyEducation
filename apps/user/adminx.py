#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Yang Zhang
# site:

import xadmin
from xadmin import views

from .models import UserProfile, EmailVerifyRecord, Banner


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '知识付费网后台管理系统'
    site_footer = '知识付费网'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time', 'created_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time', 'created_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'created_time', 'last_modified_time']
    search_fields = ['title', 'image', 'url', 'index', ]
    lsit_filter = ['title', 'image', 'url', 'index', 'created_time', 'last_modified_time']


xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
