# -*- coding: utf-8 -*-
#公共基类表单
from wtforms import Form

class BaseForm(Form):
    def get_error(self):
        message = self.errors.values()
        message = tuple(message)
        return message