import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.urls import reverse
from django.views.generic.base import View

from course.models import Course
from operation.models import UserMessage, UserCourse, UserFavorite
from organization.models import CourseOrganization, Teacher
from pure_pagination import Paginator, PageNotAnInteger
from user.forms import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm, ImageUploadForm, UserInfoForm
from utils.mixin_utils import LoginRequiredMixin
from .models import UserProfile, EmailVerifyRecord, Banner
from utils.email_send import send_register_email


class CustomizedBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# Create your views here.
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'user/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            if UserProfile.objects.filter(email=username):
                return render(request, 'user/register.html', {'register_form': register_form, 'msg': '用户已经存在'})
            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()

            # 写入欢迎注册信息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎光临本站'
            user_message.save()

            send_register_email(username, 'register')
            return render(request, 'user/login.html', {})
        else:
            return render(request, 'user/register.html', {'register_form': register_form})


class UserActiveView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'user/active_fail.html', {})
        return render(request, 'user/login.html', {})


# 用户登出
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return render(request, 'user/login.html', {'msg': '用户账户未激活!'})
            else:
                return render(request, 'user/login.html', {'msg': '用户名或密码错误!'})
        else:
            return render(request, 'user/login.html', {'login_form': login_form})


class ForgetPasswordView(View):
    def get(self, request):
        forget_password_form = ForgetPasswordForm()
        return render(request, 'user/forgetpwd.html', {'forget_password_form': forget_password_form})

    def post(self, request):
        forget_password_form = ForgetPasswordForm(request.POST)
        if forget_password_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'common/send_success.html')
        else:
            return render(request, 'user/forgetpwd.html', {'forget_password_form': forget_password_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'user/password_reset.html', {'email': email})
        else:
            return render(request, 'user/active_fail.html')
        return render(request, 'user/login.html')


# 修改用户密码
class ModifyPwdView(View):
    def post(self, request):
        reset_password_form = ResetPasswordForm(request.POST)
        if reset_password_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if password1 != password2:
                return render(request, 'user/password_reset.html', {'email': email, 'msg': '密码不一致'})

            user = UserProfile.objects.get(email=email)
            user.password = make_password(password1)
            user.save()
            return render(request, "user/login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "user/password_reset.html",
                          {"email": email, "reset_password_form": reset_password_form})


# 个人中心 - 用户个人信息
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter/usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


# 个人中心 - 用户修改头像
class ImageUploadView(LoginRequiredMixin, View):
    def post(self, request):
        # 使用传统方法
        # image_upload_form = ImageUploadForm(request.POST, request.FILES)
        # if image_upload_form.is_valid():
        #     avatar = image_upload_form.cleaned_data['avatar']
        #     request.user.avatar = avatar
        #     request.user.save()

        # 使用 ModelForm，直接传入 instance 实例对象
        image_upload_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_upload_form.is_valid():
            image_upload_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"success"}', content_type='application/json')


# 个人中心 - 修改用户密码
class PasswordUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        reset_password_form = ResetPasswordForm(request.POST)
        if reset_password_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"success", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='applicaton/json')
        else:
            return HttpResponse(json.dumps(reset_password_form.errors), content_type='application/json')


# 用户中心 - 发送邮箱验证码View
class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"注册邮箱已经存在"}', content_type='application/json')

        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success", "msg":"邮箱验证码发送成功"}', content_type='application/json')


# 用户中心 - 验证邮箱验证码 （用户需要登录，并在用户中心输入邮箱验证码）
class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


# 用户中心 - 我的课程
class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter/usercenter-mycourse.html', {
            'user_courses': user_courses,
        })


# 用户中心 - 我收藏的机构
class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        # org_list = [] # 一般写法
        # fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # for fav_org in fav_orgs:
        #     org_id = fav_org.fav_id
        #     org = CourseOrganization.objects.get(id=org_id)
        #     org_list.append(org)
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        fav_ids = [fav_org.fav_id for fav_org in fav_orgs]
        org_list = CourseOrganization.objects.filter(id__in=fav_ids)
        return render(request, 'usercenter/usercenter-fav-org.html', {
            'org_list': org_list
        })


# 用户中心 - 我收藏的讲师
class MyFavTeacher(LoginRequiredMixin, View):
    def get(self, request):
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        fav_ids = [fav_teacher.fav_id for fav_teacher in fav_teachers]
        teacher_list = Teacher.objects.filter(id__in=fav_ids)
        return render(request, 'usercenter/usercenter-fav-teacher.html', {
            'teacher_list': teacher_list
        })


# 用户中心 - 我收藏的课程
class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        fav_ids = [fav_course.fav_id for fav_course in fav_courses]
        course_list = Course.objects.filter(id__in=fav_ids)
        return render(request, 'usercenter/usercenter-fav-course.html', {
            'course_list': course_list
        })


# 用户中心 - 发送邮箱验证码（更新注册邮箱）
class UserMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_messages = UserMessage.objects.all().filter(user=request.user.id)

        # 用户进入消息后，清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 分页代码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, per_page=5, request=request)
        messages = p.page(page)
        return render(request, 'usercenter/usercenter-message.html', {
            'messages': messages,
        })


# 首页
class IndexView(View):
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrganization.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


# 全局404处理函数
def page_not_found(request, exception):
    from django.shortcuts import render_to_response
    response = render_to_response('common/404.html', {})
    response.status_code = 404
    return response


# 全局500处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('common/500.html', {})
    response.status_code = 500
    return response