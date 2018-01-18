# -*- coding: utf-8 -*-
#中间模块解决模块互相调用情况
#
#

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()