from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic.base import View

from operation.models import UserFavorite, CourseComment, UserCourse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from utils.mixin_utils import LoginRequiredMixin
from .models import Course, CourseResource, Video


class CourtListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-created_time')

        # 课程搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)
                                             | Q(desc__icontains=search_keywords)
                                             | Q(detail__icontains=search_keywords))

        # 课程列表页排序功能
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            page = 1
        p = Paginator(all_courses, per_page=6, request=request)
        courses = p.page(page)

        # 热门课程
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        return render(request, 'course/course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


# 课程详情页
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 增加课程点击数一次
        course.click_nums += 1
        course.save()

        # 是否收藏课程
        has_fav_course = False
        # 是否收藏机构
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 展示相关推荐课程
        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(Q(tag=tag) and ~Q(id=course_id))[:1]
        else:
            related_courses = []

        return render(request, 'course/course-detail.html', {
            'course': course,
            'related_courses': related_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class CourseVideoListView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 学习过该课程的同学还学过 --
        user_courses = UserCourse.objects.filter(course=course)  # 学习过该课程的所有学员们
        user_ids = [user_course.user.id for user_course in user_courses]  # 所有学员ID
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 所有学员还学过别的课程
        # 取出所有课程ID
        course_ids = [user_course.course.id for user_course in all_user_courses]  # 取出所有课程ID
        # 获取该用户学过的其它课程
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]  # 获取相关课程-前5个

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course/course_video_list.html', {
            'course': course,
            'course_resources': all_resources,
            'related_courses': related_courses,
        })


class CourseCommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComment.objects.filter(course=course)
        return render(request, 'course/course-comment.html', {
            'course': course,
            'course_resources': all_resources,
            'all_comments': all_comments,
        })


# 用户添加课程评论
class CourseAddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if bool(course_id) and bool(comments):
            course_comment = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


# 视频播放页面
class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))

        course = video.lesson.course
        course.students += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 学习过该课程的同学还学过 --
        user_courses = UserCourse.objects.filter(course=course)  # 学习过该课程的所有学员们
        user_ids = [user_course.user.id for user_course in user_courses]  # 所有学员ID
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 所有学员还学过别的课程
        # 取出所有课程ID
        course_ids = [user_course.course.id for user_course in all_user_courses]  # 取出所有课程ID
        # 获取该用户学过的其它课程
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]  # 获取相关课程-前5个

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course/course-play.html', {
            'course': course,
            'course_resources': all_resources,
            'related_courses': related_courses,
            'video': video,
        })
