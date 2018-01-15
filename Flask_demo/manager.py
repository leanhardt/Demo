# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from Flask_demo import app
from exts import db
from apps.cms.models import CMSUser

manager = Manager(app)
#用来绑定app和db到flask_migrate
Migrate(app,db)
#添加migrate的所有子命令到db下
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()