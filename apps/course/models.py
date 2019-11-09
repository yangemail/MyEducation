from django.db import models


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='课程名称')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=3, verbose_name='课程难度')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', max_length=100, verbose_name='封面图')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='章节名称')
    course = models.ForeignKey(Course, on_delete=models.SET_DEFAULT, default=0, verbose_name='课程外键')
    created_tiem = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modifed_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name='视频名称')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_DEFAULT, default=0, verbose_name='章节外键')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modifed_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    name = models.CharField(max_length=100, verbose_name='资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', max_length=100, verbose_name='资源文件')
    course = models.ForeignKey(Course, on_delete=models.SET_DEFAULT, default=0, verbose_name='课程外键')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
