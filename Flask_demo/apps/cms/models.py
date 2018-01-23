# -*- coding: utf-8 -*-
# 模版模块

from exts import db
from sqlalchemy import Column,String,Integer
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class CMSPersmission(object):
    # 255的二进制方式来表示 1111 1111
    #1.所有权限
    ALL_PERMISSION = 0b11111111
    #2.访问者的权限
    VISITOR        = 0b00000001
    #3.管理帖子的权限
    POSTER         = 0b00000010
    #4.管理评论的权限
    COMMENTER      = 0b00000100
    #5.管理板块的权限
    BOARDER        = 0b00001000
    #6.管理前台的权限
    FRONTUSER      = 0b00010000
    #7.管理后台的权限
    CMSUSER        = 0b00100000
    #8.后台管理员的权限
    ADMIN          = 0b01000000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True)
)

class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200),nullable=True)
    create_time = db.Column(db.DateTime,default=datetime.now())
    permissions = db.Column(db.Integer,default=CMSPersmission.VISITOR)

    users = db.relationship('CMSUser',secondary=cms_role_user,backref='roles')

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

    #用户权限
    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions
        return all_permissions

    #用户是否具有某个权限
    def has_permission(self, permission):
        # all_permission = self.permissions
        # result = all_permission&permission == permission
        # return result
        return self.permissions & permission == permission

    #是否是开发者权限
    @property
    def is_developer(self):
        return self.has_permission(CMSPersmission.ALL_PERMISSION)




