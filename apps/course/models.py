from django.db import models
from DjangoUeditor.models import UEditorField

from organization.models import CourseOrganization, Teacher


# Create your models here.
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrganization, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name='课程机构')
    name = models.CharField(max_length=50, verbose_name='课程名称')
    type = models.CharField(choices=((1, '实战课'), (2, '免费课'), (0, '其他')), max_length=1, default=0, verbose_name='课程类型')
    price = models.PositiveSmallIntegerField(default=0, verbose_name='价格')
    volumn = models.PositiveIntegerField(default=0, verbose_name='销量')
    online = models.DateField(null=True, blank=True, verbose_name='本课程上线时间')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    # tag = models.CharField(max_length=10, default='', verbose_name='机构标签')
    # detail = models.TextField(verbose_name='课程详情') # 更改为富文本
    detail = UEditorField(width=600, height=300, toolbars='full', imagePath="courses/ueditor/",
                          filePath="courses/ueditor/",
                          upload_settings={'imageMaxSize': 1204000}, settings={}, command=None, blank=True,
                          default='', verbose_name="课程详情")
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')  # 课程轮播图广告位
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=3, verbose_name='课程难度')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', max_length=200, null=True, blank=True, verbose_name='封面图')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(max_length=20, default='', verbose_name='课程类别')
    tag = models.CharField(max_length=10, default='', verbose_name='课程标签')
    youneed_know = models.CharField(max_length=300, default='', verbose_name='课程须知')
    teacher_tell = models.CharField(max_length=300, default='', verbose_name='老师告诉你')

    # 使用ForeignKey，对应讲师信息表（父表）
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='授课教师外键')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    # 获取课程章节数
    def get_zj_nums(self):
        return self.lesson_set.all().count()

    # get_zj_nums.short_description = '章节数' # 用于在xadmin中，显示header

    # 在xadmin中加入其他网站跳转
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="http://bing.com">跳转</a>')

    go_to.short_description = '跳转'

    # 获得学习用户
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    # 获取课程所有章节
    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return f"{self.get_type_display()} - {self.name}"
        # return "{} - {}".format(self.get_type_display(), self.title) # 相当于format本语句，f属于python3的新特性


# 首頁輪播課程
class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True  # 必须设定为 Proxy = True, 否则会另外生成一张表


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='章节名称')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='课程外键')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    # 获取章节视频
    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name='视频名称')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='章节外键')
    url = models.CharField(max_length=100, default='', null=True, blank=True, verbose_name='视频访问地址')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
    local_video_file = models.FileField(upload_to='course/video/%Y/%m', default='', null=True, blank=True,
                                        verbose_name='本地视频')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 課程上傳資源（課程相關文件）
class CourseResource(models.Model):
    name = models.CharField(max_length=100, verbose_name='资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', max_length=100, verbose_name='资源文件')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='课程外键')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
