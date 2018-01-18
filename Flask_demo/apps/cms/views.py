# -*- coding: utf-8 -*-

from flask import (
    Blueprint,
    views,
    request,
    session,
    redirect,
    url_for,
    g)
from flask import render_template
from .forms import LoginForm,ResetpwdForm
from .models import CMSUser
from .decorators import login_required
import config
from exts import db,mail
from utils import restful
from flask_mail import Message

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

@bp.route('/email/')
def send_email():
    msg = Message("我爱佳佳",recipients=['116592436@qq.com','893607696@qq.com'],body='测试')
    mail.send(msg)
    return 'success'

#个人信息
@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')

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
            message = form.get_error()
            return render_template('cms/cms_login.html',message=message)
#修改密码
class ResetpwdView(views.MethodView):
    decorators = [login_required]

    def get(self,message=None):
        return render_template('cms/cms_resetpwd.html',message=message)

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success(message="success",data=None)
            else:
                return restful.parma_error("密码错误")
        else:
            message = form.get_error()
            return restful.parma_error(form.get_error())

class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')
    def post(self):
        pass

bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetpwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))
