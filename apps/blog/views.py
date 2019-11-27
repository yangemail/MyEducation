from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from blog.models import Tutorial, Article, Category
from operation.models import UserFavorite, UserTutorial, TutorialComment
from pure_pagination import Paginator


class ArticleIndexView(View):
    def get(self, request):
        return render(request, 'blog/article_index.html', {})


class ArticleListView(View):
    # 文章列表页
    def get(self, request):
        # 全部父级分类
        all_p_categories = Category.objects.all().filter(parent_category__isnull=True)
        # 全部子级分类
        all_c_categories = Category.objects.all().filter(parent_category__isnull=False)
        # 全部文章
        all_articles = Article.objects.all()

        # 总点击次数
        hot_articles = all_articles.order_by('-click_nums')[:10]

        # 取出parent category id
        p_category_id = request.GET.get('p_category', '')
        if p_category_id:
            p_category = Category.objects.get(id=int(p_category_id))
            all_c_categories = all_c_categories.filter(parent_category=p_category)
            all_articles = all_articles.filter(category__in=all_c_categories)

        c_category_id = request.GET.get('c_category', '')
        if c_category_id:
            c_category = Category.objects.get(id=int(c_category_id))
            all_articles = all_articles.filter(category=c_category)

        # 计算实际返回文章数量
        article_nums = all_articles.count()

        # 对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            page = 1
        p = Paginator(all_articles, per_page=2, request=request)
        articles = p.page(page)

        return render(request, 'blog/article_list.html', {
            'all_p_categories': all_p_categories,
            'p_category_id': p_category_id,
            'all_c_categories': all_c_categories,
            'c_category_id': c_category_id,
            'all_articles': articles,
            'article_nums': article_nums,
            'hot_articles': hot_articles,
        })


class ArticleDetailView(View):
    def get(self, request, article_id):
        article = Article.objects.get(id=int(article_id))

        # 增加一次文章点击数
        article.click_nums += 1
        article.save()

        # 是否收藏文章
        has_fav_article = False
        # 是否收藏机构
        has_fav_org = False

        # 展示相关推荐文章
        tag_list = article.tag
        if tag_list:
            related_articles = Article.objects.filter(Q(tag__in=tag_list) and ~Q(id=article.id))[:5]
        else:
            related_articles = []

        return render(request, 'blog/article_detail.html', {
            'article': article,
            'related_articles': related_articles,
        })


class TutorialListView(View):
    def get(self, request):
        # 默认展示排序为：按最新添加时间排序
        all_tutorials = Tutorial.objects.all().order_by('-created_time')

        # 教程搜索功能 - 首页
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_tutorials = all_tutorials.filter(Q(title__icontains=search_keywords)
                                                 | Q(desc__icontains=search_keywords)
                                                 | Q(detail__icontains=search_keywords))

        # 教程列表页排序功能
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_tutorials = all_tutorials.order_by('-click_nums')
            elif sort == 'students':
                all_tutorials = all_tutorials.order_by('-students')

        # 对教程进行分页
        try:
            page = request.GET.get('page', 1)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            page = 1
        p = Paginator(all_tutorials, per_page=2, request=request)
        tutorials = p.page(page)

        # 热门教程
        hot_tutorials = Tutorial.objects.all().order_by('-click_nums')[:3]

        return render(request, 'blog/tutorial_list.html', {
            'all_tutorials': tutorials,
            'sort': sort,
            'hot_tutorials': hot_tutorials,
        })


# 教程详情页
class TutorialDetailView(View):
    def get(self, request, tutorial_id):
        tutorial = Tutorial.objects.get(id=int(tutorial_id))

        # 增加“教程”点击数一次
        tutorial.click_nums += 1
        tutorial.save()

        # 是否收藏教程
        has_fav_tutorial = False
        # 是否收藏机构
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=tutorial.id, fav_type=4):
                has_fav_tutorial = True
            if UserFavorite.objects.filter(user=request.user, fav_id=tutorial.tutorial_org.id, fav_type=2):
                has_fav_org = True

        # 展示相关推荐教程
        tag_list = tutorial.tag
        if tag_list:
            related_tutorials = Tutorial.objects.filter(Q(tag__in=tag_list) and ~Q(id=tutorial.id))[:2]
        else:
            related_tutorials = []

        return render(request, 'blog/tutorial_detail.html', {
            'tutorial': tutorial,
            'related_tutorials': related_tutorials,
            'has_fav_tutorial': has_fav_tutorial,
            'has_fav_org': has_fav_org,
        })


class TutorialArticleListView(View):
    def get(self, request, tutorial_id):
        tutorial = Tutorial.objects.get(id=int(tutorial_id))
        tutorial.students += 1
        tutorial.save()

        # 查询用户是否已经关联了该教程
        user_tutorial = UserTutorial.objects.filter(user=request.user, tutorial=tutorial)
        if not user_tutorial:
            user_tutorial = UserTutorial(user=request.user, tutorial=tutorial)
            user_tutorial.save()

        # 学习过该课程的同学还学习过的课程
        user_tutorials = UserTutorial.objects.filter(tutorial=tutorial)  # 学习过该教程的所有的同学
        user_ids = [user_tutorial.user.id for user_tutorial in user_tutorials]  # 获取学习过该课程的同学们的ID
        all_user_tutorials = UserTutorial.objects.filter(user_id__in=user_ids)  # 获取以上学员学习的全部教程
        # 取出所有教程ID
        tutorial_ids = [user_tutorial.tutorial.id for user_tutorial in all_user_tutorials]
        # 获取用户学过的其它课程-前5个
        related_tutorials = Tutorial.objects.filter(id__in=tutorial_ids).order_by('-click_nums')[:5]

        # TODO: 通过文章添加 resources
        return render(request, 'blog/tutorial_ariticle_list.html', {
            'tutorial': tutorial,
            'related_tutorials': related_tutorials,
        })


class TutorialCommentsView(View):
    def get(self, request, tutorial_id):
        tutorial = Tutorial.objects.get(id=int(tutorial_id))

        # 学习过该课程的同学还学习过的课程
        user_tutorials = UserTutorial.objects.filter(tutorial=tutorial)  # 学习过该教程的所有的同学
        user_ids = [user_tutorial.user.id for user_tutorial in user_tutorials]  # 获取学习过该课程的同学们的ID
        all_user_tutorials = UserTutorial.objects.filter(user_id__in=user_ids)  # 获取以上学员学习的全部教程
        # 取出所有教程ID
        tutorial_ids = [user_tutorial.tutorial.id for user_tutorial in all_user_tutorials]
        # 获取用户学过的其它课程-前5个
        related_tutorials = Tutorial.objects.filter(id__in=tutorial_ids).order_by('-click_nums')[:5]

        # TODO: Add resources
        all_comments = TutorialComment.objects.filter(tutorial=tutorial)
        return render(request, 'blog/tutorial_comment.html', {
            'tutorial': tutorial,
            'all_comments': all_comments,
            'related_tutorials': related_tutorials,
        })
