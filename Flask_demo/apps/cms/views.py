# -*- coding: utf-8 -*-

from flask import Blueprint,request
from flask import render_template
from .forms import CMSForm

bp = Blueprint('cms',__name__,url_prefix='/cms')

@bp.route('/',methods=['GET','POST'])
def index():
    form = CMSForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        print(username)
    return render_template('cms/index.html')