from django.db import models

# Create your models here.
from DjangoUeditor.models import UEditorField
from course.models import Video
from organization.models import Teacher, CourseOrganization
from user.models import UserProfile


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Category(models.Model):
    CATEGORY_TYPE = (
        (1, '方向'),  # 例如：前端开发,后端开发,移动开发,计算机基础,前沿技术,云计算&大数据,运维&测试,数据库,UI设计&多媒体,游戏，等
        (2, '技术栈'),  # 例如：计算机网络，HTML/CSS，JavaScript，Vue.js，React.JS，Angular，Node.js，jQuery，小程序，前端工具，Java，等
        # (3, '三级目录'), # 暂时不需要
    )
    name = models.CharField(max_length=30, default='', verbose_name='分类名称')
    desc = models.TextField(max_length=200, default='', verbose_name='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='类目级别')
    parent_category = models.ForeignKey('self', related_name='sub_category', on_delete=models.SET_NULL, null=True,
                                        blank=True, verbose_name='父级分类')
    is_tab = models.BooleanField(default=False, verbose_name='是否导航')
    index = models.PositiveSmallIntegerField(default=999, verbose_name='显示顺序（从小到大）')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return '分类：{} - 父级分类：{}'.format(self.name,
                                        self.parent_category.name if self.parent_category is not None else '无父级分类')


class Tutorial(models.Model):
    tutorial_org = models.ForeignKey(CourseOrganization, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name='教程机构')
    title = models.CharField(max_length=50, verbose_name='教程标题')
    desc = models.CharField(max_length=300, verbose_name='课程描述')  # 用于SEO
    detail = UEditorField(width=600, height=300, toolbars='full', imagePath="tutorials/ueditor/",
                          filePath="tutorials/ueditor/",
                          upload_settings={'imageMaxSize': 1204000}, settings={}, command=None, blank=True,
                          default='', verbose_name="教程详情")
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2, default='cj',
                              verbose_name='课程难度')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', max_length=200, null=True, blank=True, verbose_name='封面图')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='教程分类')  # 教程分类
    tag = models.ManyToManyField(Tag, verbose_name='文章标签')  # 課程與標籤是多對多的關係
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最後修改時間')

    class Meta:
        verbose_name = '教程'
        verbose_name_plural = verbose_name

    def get_articles(self):
        article_list = []
        for section in self.section_set.all():
            for article in section.article_set.all():
                article_list.append(article)
        return article_list

    def get_articles_count(self):
        return len(self.get_articles())

    def __str__(self):
        return self.title


class Section(models.Model):
    name = models.CharField(max_length=100, verbose_name='章节名称')
    tutorial = models.ForeignKey(Tutorial, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tutorial外键')
    index = models.PositiveSmallIntegerField(default=999, verbose_name='排序')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "章节名称：{} - 教程名称：{}".format(self.name, self.tutorial.title)


# 獲得文章存檔YYYY/MM，年、月
class ArticleManager(models.Manager):
    def distinct_date_to_year_and_month(self):
        distinct_date_list = []
        date_list = self.values('created_time')
        for date in date_list:
            date_str = date['created_time'].strftime('%Y/%m')
            if date_str not in distinct_date_list:
                distinct_date_list.append(date_str)
            return distinct_date_list


class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章標題')
    excerpt = models.CharField(max_length=200, blank=True, null=True, verbose_name='文章摘要')
    content = UEditorField(width=600, height=300, toolbars='full', imagePath="articles/ueditor/",
                           filePath="articles/ueditor/",
                           upload_settings={'imageMaxSize': 1204000}, settings={}, command=None, blank=True,
                           default='', verbose_name="文章详情")
    click_nums = models.IntegerField(default=0, verbose_name='點擊次數')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推薦（文章）')
    # 用戶外鍵（文章由用戶添加） - 文章作者
    # user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='多用戶添加外鍵')
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='文章視頻')  # 多篇文章可能對應一個視頻
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='教程分类')  # 教程分类
    section = models.ManyToManyField(Section, verbose_name='章节外键-多对多')
    # 教師外鍵（文章由教師添加） - 文章作者
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='授课教师外键')
    tag = models.ManyToManyField(Tag, verbose_name='文章标签')  # 課程與標籤是多對多的關係
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最後修改時間')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title



