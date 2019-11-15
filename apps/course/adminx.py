#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Yang Zhang
# site:

import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse


# xadmin in-line admin
# class LessonInline(object):
#     model = Lesson
#     extra = 0

# class CourseResourceInline(object):
#     model = CourseResource
#     extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'created_time', 'last_modified_time']  # 此处也可以加入函数，例如：get_zj_nums
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', ]
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'created_time', 'last_modified_time']
    # ordering = ['-click_nums'] # 排序 xadmin 显示页面
    # readonly_fields = ['click_nums'] # 设置xadmin中只读字段
    # exclude = ['fav_nums'] # 设置xadmin中不显示字段 （与上面的readonly_fields不能同时使用一个字段）
    # inlines = [LessonInline, CourseResourceInline] # 可以在本页面直接添加章节信息了
    # list_editable = ['degree', 'desc'] # 在列表页可以对字段进行直接修改了，不用在进入编辑界面
    # refresh_times = [3, 5]  # 设定xadmin页面刷新频率，生成刷新图标
    style_fields = {'detail': 'ueditor'}  # 指明"detail"使用"ueditor"， 注意这里是detail字段是富文本字段的名称

    # 对列表中的数据进行过滤
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    # 重载xadmin中的 save_models(self)方法，在save中加入自己的逻辑
    # 例如：在xadmin中，保存课程的时候，统计课程机构的课程数（新增、修改都会走这个接口）
    def save_models(self):
        obj = self.new_obj
        obj.save()  # 对当前实例先进行保存，然后再发起运算步骤
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'created_time', 'last_modified_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', ]
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'created_time', 'last_modified_time']

    # 对列表中的数据进行过滤
    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['name', 'course', 'created_time', 'last_modified_time']
    search_fields = ['name', 'course', ]
    list_filter = ['name', 'course__name', 'created_time', 'last_modified_time']


class VideoAdmin(object):
    list_display = ['name', 'lesson', 'created_time', 'last_modified_time']
    search_fields = ['name', 'lesson', ]
    list_filter = ['name', 'lesson', 'created_time', 'last_modified_time']


class CourseResourceAdmin(object):
    list_display = ['name', 'download', 'course', 'created_time', 'last_modified_time']
    search_fields = ['name', 'download', 'course', ]
    list_filter = ['name', 'download', 'course', 'created_time', 'last_modified_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
