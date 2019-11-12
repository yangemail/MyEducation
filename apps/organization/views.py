from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

from organization.forms import UserAskForm

from organization.models import CourseOrganization, City
from course.models import Course


class OrgView(View):
    # 机构列表功能
    def get(self, request):
        # 城市
        all_cities = City.objects.all()

        # 机构课程
        all_orgs = CourseOrganization.objects.all()
        # 热门机构
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

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

        return render(request, 'org-list.html',
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
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html',
                      {'all_courses': all_courses,
                       'all_teachers': all_teachers,
                       'course_org': course_org,
                       'current_page': current_page, })


# 机构课程列表页
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrganization.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrganization.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrganization.objects.get(id=org_id)
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html',
                      {'all_teachers': all_teachers,
                       'course_org': course_org,
                       'current_page': current_page,
                       })
