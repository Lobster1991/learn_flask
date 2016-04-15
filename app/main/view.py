# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    Flask会为蓝本中的全部端点加上一个命名空间（Blueprint构造函数的第一个参数），\
    这样在不同的蓝本中使用相同的端点名定时视图函数就不会产生冲突。              \
    视图函数index()注册的端点名是main.index，其URL使用url)for('main.index')获取。
    """
    form = NameForm()
    if form.validate_on_submit():
        # ...
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())