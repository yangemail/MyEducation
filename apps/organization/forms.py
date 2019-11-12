#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Yang Zhang
# site:

import re
from django import forms

from operation.models import UserAsk


# class UserAskForm(forms.Form): # 传统form
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=5, max_length=50)


class UserAskForm(forms.ModelForm): # ModelForm与Model进行整合
    # my_field = forms.CharField() # 可以另外添加field
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self): #自定义ModelForm表单验证，必须以clean_开头
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')