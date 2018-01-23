# -*- coding: utf-8 -*-
#装饰器文件

from flask import session,redirect,url_for,g
from functools import wraps
import config

#登陆验证
def login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if config.CMS_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))
    return inner

#权限验证
def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args,**kwargs):
            user = g.cms_user
            #用户是否有访问该页面的权限,有则跳转，没有跳转首页
            if user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter