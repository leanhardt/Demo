# -*- coding: utf-8 -*-
# 表单验证模块

from wtforms import StringField,IntegerField,ValidationError
from ..forms import BaseForm
from wtforms.validators import InputRequired,Length,Email,EqualTo
from utils import cache
from flask import g


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20,message='密码长度为6-20位'),InputRequired(message='请输入密码')])
    remember = IntegerField()

class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='旧密码长度为6-20位')])
    newpwd = StringField(validators=[Length(6, 20, message='新密码长度为6-20位!')])
    newpwd2 = StringField(validators=[EqualTo('newpwd',message='新密码不一致')])

    def validate_newpwd(self,field):
        newpwd = field.data
        oldpwd = self.oldpwd.data
        if newpwd == oldpwd:
            raise ValidationError('新密码与旧密码一致！')

class ResetemailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式！')])
    captcha = StringField(validators=[Length(min=6,max=6,message='请输入6位验证码！')])

    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = cache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误！')

    def validate_email(self,field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('不能修改为相同的邮箱！')
