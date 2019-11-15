from django.db import models


class City(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市')
    desc = models.CharField(max_length=200, verbose_name='描述')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# Create your models here.
class CourseOrganization(models.Model):
    name = models.CharField(max_length=50, verbose_name='机构名称')
    tag = models.CharField(max_length=10, default='全国知名', verbose_name='机构标签')
    desc = models.TextField(verbose_name='机构描述')
    category = models.CharField(max_length=20, choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')), default='pxjg',
                                verbose_name='机构类别')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', max_length=100, verbose_name='机构logo')
    address = models.CharField(max_length=150, verbose_name='机构地址')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所在城市外键')
    student_nums = models.IntegerField(default=0, verbose_name='学习人数')
    course_nums = models.IntegerField(default=0, verbose_name='课程数')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    # 获取课程机构的教师数量
    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name='教师名称')
    avatar = models.ImageField(upload_to='teacher/%Y/%m', default='avatar/default.png', max_length=100,
                               verbose_name='用户头像')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='公司职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    courseorganization = models.ForeignKey(CourseOrganization, on_delete=models.SET_NULL, null=True, blank=True,
                                           verbose_name='所属机构外键')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '机构教师'
        verbose_name_plural = verbose_name

    def org(self):
        return self.courseorganization

    def get_course_nums(self):
        return self.course_set.all().count()

    def __str__(self):
        return self.name
