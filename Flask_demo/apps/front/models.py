# -*- coding: utf-8 -*-

from exts import db
import shortuuid
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(50),primary_key=True,default=shortuuid.uuid)
    telephone = db.Column(db.String(11),nullable=False,unique=True)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    join_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,*args,**kwargs):
        if 'password' in kwargs:
            self._password = kwargs.get('password')
        

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self,raw_password):
        return check_password_hash(self.password,raw_password)



