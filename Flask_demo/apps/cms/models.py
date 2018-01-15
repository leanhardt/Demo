# -*- coding: utf-8 -*-
# 模版模块

from exts import db
from sqlalchemy import Column,String,Integer


class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column('id',db.Integer,primary_key=True)
    username = db.Column('username',db.String(20))
    phone = db.Column('phone',db.String(11))
    email = db.Column('email',db.String(20))
    password = db.Column('password',db.String(10),default='111111')