from django.db import models

from blog.models import Tutorial, Article
from user.models import UserProfile
from course.models import Course


# Create your models here.
class UserAsk(models.Model):
    name = models.CharField(max_length=50, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    course_name = models.CharField(max_length=50, verbose_name='课程名称')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


class CourseComment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='用户外键')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='课程外键')
    comments = models.CharField(max_length=200, verbose_name='课程评论')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class TutorialComment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='用戶外鍵')  # 進行評論必須登錄， 否則會有垃圾信息
    tutorial = models.ForeignKey(Tutorial, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='文章外键')  # 評論文章外鍵
    comments = models.TextField(verbose_name='评论内容')
    pid = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='父级评论')  # 對於父級評論的回復
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    class Meta:
        verbose_name = '教程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


class ArticleComment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='用戶外鍵')  # 進行評論必須登錄， 否則會有垃圾信息
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='文章外键')  # 評論文章外鍵
    comments = models.TextField(verbose_name='评论内容')
    pid = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='父级评论')  # 對於父級評論的回復
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    class Meta:
        verbose_name = '文章评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='用户外键')
    fav_id = models.IntegerField(default=0, verbose_name='收藏数据ID')
    fav_type = models.IntegerField(choices=((1, '课程'), (2, '课程机构'), (3, '讲师'), (4, '教程'), (5, '文章')), default=5,
                                   verbose_name='收藏类型')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name='接收用户')
    message = models.CharField(max_length=500, verbose_name='消息内容')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


# 多对多的中间表： 学生对课程-多对多
class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='用户外键')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='课程外键')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name


# 多对多中间表： 学生对教程 - 多对多
class UserTutorial(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, default=True, verbose_name='用户外键')
    tutorial = models.ForeignKey(Tutorial, on_delete=models.SET_NULL, null=True, default=True, verbose_name='教程外键')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户教程'
        verbose_name_plural = verbose_name
