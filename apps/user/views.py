import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.urls import reverse
from django.views.generic.base import View

from operation.models import UserMessage
from user.forms import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm, ImageUploadForm, UserInfoForm
from utils.mixin_utils import LoginRequiredMixin
from .models import UserProfile, EmailVerifyRecord
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
                    return render(request, 'index.html', {})
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


# 用户中心 - 发送邮箱验证码（更新注册邮箱）
class UserUserMessageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter/usercenter-message.html', {})
