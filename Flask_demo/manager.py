# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from Flask_demo import create_app
from exts import db
from apps.cms import models as cms_models

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

if __name__ == '__main__':
    manager.run()