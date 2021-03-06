from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.db.models import Q

from organization.forms import UserAskForm

from organization.models import CourseOrganization, City, Teacher
from course.models import Course
from operation.models import UserFavorite


class OrgListView(View):
    # 机构列表功能
    def get(self, request):
        # 城市
        all_cities = City.objects.all()

        # 机构课程
        all_orgs = CourseOrganization.objects.all()

        # 热门机构
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # 机构搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords)
                                       | Q(desc__icontains=search_keywords))

        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 筛选功能
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-student_nums')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 计算实际返回数量
        org_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            page = 1
        p = Paginator(all_orgs, per_page=5, request=request)
        orgs = p.page(page)

        return render(request, 'org/org-list.html',
                      {'all_orgs': orgs,
                       'org_nums': org_nums,
                       'all_cities': all_cities,
                       'city_id': city_id,
                       'category': category,
                       'hot_orgs': hot_orgs,
                       'sort': sort, })


# 用户添加咨询
class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


# 机构首页
class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrganization.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 记录是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org/org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


# 机构课程列表页
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrganization.objects.get(id=int(org_id))

        # 标识已收藏、未收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()
        return render(request, 'org/org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrganization.objects.get(id=int(org_id))

        # 收藏、已收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org/org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrganization.objects.get(id=org_id)

        # 收藏、已收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teachers = course_org.teacher_set.all()
        return render(request, 'org/org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


# 用户收藏机构，或取消收藏
class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户登录状态
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        # 如果记录已经存在，则取消收藏
        if exist_record:
            exist_record.delete()
            # 取消收藏后，Course的fav_nums需要减一
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums <= 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrganization.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums <= 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums <= 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                # 收藏后，Course的fav_nums需要加一
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrganization.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


# 课程讲师列表页
class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 老师搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords)
                                               | Q(work_company__icontains=search_keywords)
                                               | Q(work_position__icontains=search_keywords))

            # 按照“全部”和“人气”进行排序
            sort = request.GET.get('sort', '')
            if sort:
                if sort == 'hot':
                    all_teachers = all_teachers.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            page = 1
        p = Paginator(all_teachers, per_page=2, request=request)
        teachers = p.page(page)

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]

        return render(request, 'org/teacher-list.html', {
            'all_teachers': teachers,
            'sorted_teacher': sorted_teacher,
        })


# 课程讲师详细页
class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        # 此讲师的所有课程
        all_courses = Course.objects.filter(teacher=teacher)

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]

        # 收藏
        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
            has_teacher_faved = True
        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_id=teacher.courseorganization.id, fav_type=2):
            has_org_faved = True

        return render(request, 'org/teacher-detail.html', {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher,
            'has_teacher_faved': has_teacher_faved,
            'has_org_faved': has_org_faved,
        })
