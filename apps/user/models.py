from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from course.models import Course


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='昵称')
    # image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=100)
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=200,
                               verbose_name='用户头像')
    gender = models.CharField(choices=(('M', '男'), ('F', '女')), null=True, blank=True, max_length=1, verbose_name='性别')
    # qq = models.CharField(max_length=20, null=True, blank=True, verbose_name='QQ号码')
    mobile = models.CharField(max_length=11, null=True, blank=True, unique=True, verbose_name='手机号码')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name='地址')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')

    study_time = models.PositiveIntegerField(default='0', verbose_name='学习时长（min)')

    # course = models.ManyToManyField(Course, verbose_name='课程') # 学生与课程多对多，课程为主表，学生为子表，所以关系写到子表上
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    # 获取用户未读消息的数量
    def unread_nums(self):
        from operation.models import UserMessage # 必须这里引入，否则会发生循环引用
        return UserMessage.objects.filter(user=self.id, has_read=False).count()

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='邮箱验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱地址')
    send_type = models.CharField(choices=(('register', '注册'), ('forget', '找回密码'), ('update_email', '修改邮箱')),
                                 max_length=30, verbose_name='验证码类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name='预定义发送时间 ')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0} [{1}]'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(upload_to='banner/%Y/%m', max_length=200, verbose_name='轮播图')
    url = models.URLField(max_length=100, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='顺序')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
