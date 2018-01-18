# -*- coding: utf-8 -*-
from .views import bp
import config
from flask import session,g
from .models import CMSUser

#获取CMS用户信息保存到g对象中
@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user