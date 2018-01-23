# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from Flask_demo import create_app
from exts import db
from apps.cms import models as cms_models
from apps.cms.models import CMSPersmission,CMSUser,CMSRole

app = create_app()
CMSUser = cms_models.CMSUser

manager = Manager(app)
#用来绑定app和db到flask_migrate
Migrate(app,db)
#添加migrate的所有子命令到db下
manager.add_command('db',MigrateCommand)

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功')

#权限设置
@manager.command
def create_role():
    #1.访问者
    visitor = CMSRole(name='访问者',desc='只能读取相关数据，不能修改')
    visitor.permissions = CMSPersmission.VISITOR
    #2.运营
    operator = CMSRole(name='运营',desc='管理帖子，管理论坛，管理前台用户')
    operator.permissions = CMSPersmission.VISITOR|CMSPersmission.POSTER\
                           |CMSPersmission.COMMENTER|CMSPersmission.FRONTUSER

    #3.管理员
    admin = CMSRole(name='管理员',desc='拥有本系统所有权限')
    admin.permissions = CMSPersmission.VISITOR|CMSPersmission.POSTER|CMSPersmission.COMMENTER\
                        |CMSPersmission.CMSUSER|CMSPersmission.BOARDER|CMSPersmission.FRONTUSER

    #4.开发者
    develop = CMSRole(name='开发者',desc='开发人员专用')
    develop.permissions = CMSPersmission.ALL_PERMISSION

    db.session.add_all([visitor,operator,admin,develop])
    db.session.commit()

@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加到角色成功')
        else:
            print('没有这个角色%s'%role)
    else:
        print('%s没有这个用户'%email)

@manager.command
def test_permission():
    user = CMSUser.query.first()
    # if(user.has_permission(CMSPersmission.VISITOR)):
    if user.is_developer:
        print('这个用户有访问者权限')
    else:
        print('该用户没有访问权限')

if __name__ == '__main__':
    manager.run()