from django.db import models

# Create your models here.
from DjangoUeditor.models import UEditorField
from course.models import Video
from organization.models import Teacher
from user.models import UserProfile


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Category(models.Model):
    CATEGORY_TYPE = (
        (1, '方向'),  # 例如：前端开发,后端开发,移动开发,计算机基础,前沿技术,云计算&大数据,运维&测试,数据库,UI设计&多媒体,游戏，等
        (2, '技术栈'),  # 例如：计算机网络，HTML/CSS，JavaScript，Vue.js，React.JS，Angular，Node.js，jQuery，小程序，前端工具，Java，等
        # (3, '三级目录'), # 暂时不需要
    )
    name = models.CharField(max_length=30, default='', verbose_name='分类名称')
    desc = models.TextField(default='', verbose_name='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='类目级别')
    parent_category = models.ForeignKey('self', related_name='sub_category', on_delete=models.SET_NULL, null=True,
                                        blank=True, verbose_name='父级分类')
    is_tab = models.BooleanField(default=False, verbose_name='是否导航')
    index = models.PositiveSmallIntegerField(default=999, verbose_name='显示顺序（从小到大）')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')


class Tutorial(models.Model):
    title = models.CharField(max_length=50, verbose_name='標題')
    desc = models.CharField(max_length=500, verbose_name='描述')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最後修改時間')


class Section(models.Model):
    name = models.CharField(max_length=100, verbose_name='章節名稱')
    chapbook = models.ForeignKey(Tutorial, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='書的外鍵')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最後修改時間')

    class Meta:
        verbose_name = '章節'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


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
    # 教師外鍵（文章由教師添加） - 文章作者
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='授课教师外键')
    # 用戶外鍵（文章由用戶添加） - 文章作者
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='多用戶添加外鍵')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='文章分類')
    tag = models.ManyToManyField(Tag, verbose_name='文章標籤')  # 課程與標籤是多對多的關係
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='文章視頻')  # 多篇文章可能對應一個視頻
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最後修改時間')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='文章外鍵')  # 評論文章外鍵
    content = models.TextField(verbose_name='評論內容')
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='用戶外鍵')  # 進行評論必須登錄， 否則會有垃圾信息
    # username = models.CharField(max_length=200, blank=True, null=True, verbose_name='用戶名')
    # email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='郵箱地址')
    # url = models.URLField(max_length=100, blank=True, null=True, verbose_name='個人網頁地址')
    pid = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='父級評論')  # 對於父級評論的回復
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='發佈時間')

    class Meta:
        verbose_name = '評論'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)
