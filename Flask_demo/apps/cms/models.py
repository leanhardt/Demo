# -*- coding: utf-8 -*-
# 模版模块

from exts import db
from sqlalchemy import Column,String,Integer
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now())

    #处理密码
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email
    #property把password函数转化为password属性,相当与get方法
    @property
    def password(self):
        return self._password
    #set方法，generate_password_hash哈希处理密码
    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)

    #检查密码check_password_hash
    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result



