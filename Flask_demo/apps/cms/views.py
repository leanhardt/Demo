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
from .forms import LoginForm,ResetpwdForm,ResetemailForm
from .models import CMSUser
from .decorators import login_required
import config,string,random
from exts import db,mail
from utils import restful
from flask_mail import Message
from utils import cache

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

@bp.route('/email_captcha/')
def email_captcha():
    #/email_captcha/?email=xxx@xxx.com
    email = request.args.get('email')
    if not email:
        return restful.parma_error('请传递邮箱参数！')

    #获取验证码
    #string.ascii_letters获取a-zA-Z的字母列表
    source = list(string.ascii_letters)
    #加上0-9的数字到列表source
    #source = source.extend(["0","1","2","3","4","5","6","7","8","9"])
    source.extend(map(lambda x:str(x),range(0,10)))
    #从列表中随机获取6位验证码
    captcha = "".join(random.sample(source,6))

    #给这个邮箱发送邮件
    msg = Message('python论坛邮箱验证码',recipients=[email],body='邮箱验证码：%s'%captcha)
    try:
        mail.send(msg)
    except:
        return restful.server_error()
    cache.set(email,captcha)
    return restful.success()

# @bp.route('/email/')
# def send_email():
#     msg = Message("我爱佳佳",recipients=['116592436@qq.com','893607696@qq.com'],body='测试')
#     mail.send(msg)
#     return 'success'

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
        form = ResetemailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.parma_error(form.get_error())

bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetpwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))
