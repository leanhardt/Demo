# -*- coding: utf-8 -*-

from exts import db
from sqlalchemy import Column,Integer

class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.column('id',Integer,prefix_key=True)
