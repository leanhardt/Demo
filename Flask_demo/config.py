# -*- coding: utf-8 -*-
import os

DEBUG = True

#数据库连接配置
DB_USERNAME = 'root'
DB_PASSWORD = '123456'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'pytest'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.urandom(24)

#PERMANENT_SESSION_LIFETIME

#sessionID
CMS_USER_ID = 'ASDASDAAD'

#邮箱配置
#服务器邮箱地址
MAIL_SERVER = 'smtp.qq.com'
#加密方式 MAIL_USE_TLS: 端口号587
#加密方式 MAIL_USE_SSL: 端口号465
MAIL_PORT = '465'
#MAIL_USE_TLS : 默认为 False
MAIL_USE_SSL = True
#MAIL_DEBUG : 默认为 app.debug
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ''