# -*- coding: utf-8 -*-

from flask import Flask
from apps.cms import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
import config
from exts import db,mail
#CSRF保护
from flask_wtf import CSRFProtect

def create_app():
    app = Flask(__name__)
    #读取配置文件
    app.config.from_object(config)
    #绑定蓝图模块
    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    # 绑定app到db
    db.init_app(app)
    #保护app
    CSRFProtect(app)

    mail.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=8000)
