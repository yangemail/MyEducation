from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from django.db.models import Q

from operation.models import UserFavorite
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

from .models import CourseOrganization, Course, CourseResource


class CourtListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-created_time')

        # 筛选功能
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


class CourseInfoView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        return render(request, 'course/course-video.html', {
            'course': course,
        })


class CourseCommentsView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        return render(request, 'course/course-comment.html', {
            'course': course
        })
