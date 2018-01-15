# -*- coding: utf-8 -*-
# 表单验证模块

from wtforms import StringField
from wtforms.form import Form
from wtforms.validators import DataRequired,length

class CMSForm(Form):
    username = StringField('username',validators=[length(5,10)])
    phone = StringField('phone',validators=[length(11,11),DataRequired])
    password = StringField('password',validators=[length(6,10)])