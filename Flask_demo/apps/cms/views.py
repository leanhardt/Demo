# -*- coding: utf-8 -*-

from flask import Blueprint,views,request,session,redirect,url_for,g
from flask import render_template
from .forms import LoginForm
from .models import CMSUser
from .decorators import login_required
import config

bp = Blueprint('cms',__name__,url_prefix='/cms')

@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')

#注销
@bp.route('/logout/')
@login_required
def logout():
    #session.clear() 清除所有session
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))

class LoginView(views.MethodView):

    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    #如果设置session.permanent = True
                    #那么过期时间为31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return render_template('cms/cms_login.html',message='邮箱或密码错误')
        else:
            message = form.errors.popitem()[1][0]
            return render_template('cms/cms_login.html',message=message)



bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
