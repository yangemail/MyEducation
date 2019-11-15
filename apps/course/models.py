from django.db import models

from organization.models import CourseOrganization, Teacher


# Create your models here.
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrganization, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='课程机构')
    name = models.CharField(max_length=50, verbose_name='课程名称')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    tag = models.CharField(max_length=10, default='', verbose_name='机构标签')
    detail = models.TextField(verbose_name='课程详情')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播') # 课程轮播图广告位
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='授课教师外键')
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=3, verbose_name='课程难度')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', max_length=100, null=True, blank=True, verbose_name='封面图')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(max_length=20, default='', verbose_name='课程类别')
    tag = models.CharField(max_length=10, default='', verbose_name='课程标签')
    youneed_know = models.CharField(max_length=300, default='', verbose_name='课程须知')
    teacher_tell = models.CharField(max_length=300, default='', verbose_name='老师告诉你')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    # 获取课程章节数
    def get_zj_nums(self):
        return self.lesson_set.all().count()

    # 获得学习用户
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    # 获取课程所有章节
    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


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
    local_video_file = models.FileField(upload_to='course/video/%Y/%m', default='', null=True, blank=True, verbose_name='本地视频')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


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