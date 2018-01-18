# -*- coding: utf-8 -*-
# 表单验证模块

from wtforms import StringField,IntegerField
from ..forms import BaseForm
from wtforms.validators import InputRequired,Length,Email,EqualTo


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20,message='密码长度为6-20位'),InputRequired(message='请输入密码')])
    remember = IntegerField()

class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='旧密码长度为6-20位')])
    newpwd = StringField(validators=[Length(6, 20, message='新密码长度为6-20位!')])
    newpwd2 = StringField(validators=[EqualTo('newpwd',message='新密码不一致')])


