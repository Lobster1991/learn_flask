# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__) # <Flask 'hello'>
app.config['SECRET_KEY'] = "hei hei hei"
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# 每次请求结束后自动提交数据库的变动
app.config['SQLACHEMY_COMMIT_ON_TEARDOWN'] = True
#  UserWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant
#  overhead and will be disabled by default in the future.  Set it
# to True to suppress this warning.
# warnings.warn('SQLALCHEMY_TRACK_MODIFICATIONS adds significant
# overhead and will be disabled by default in the future.  Set it
# to True to suppress this warning.')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField("Submit")

class Role(db.Model):
    # "__tablename__"定义数据库中的表名，若不定义则使用SQLAlchemy的默认名。
    __tablename__ = 'roles'
    # Flask-SQLAlchemy要求每个模型都定义主键
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 'users'属性代表这个关系的面向对象视角。对于一个Role类的实例，其users \
    # 属性将返回与角色关联的用户组成的列表。db.relationship的第一个参数 \
    # 'User'表明这个关系的另一端的模型是'User’。
    # backref参数像'User'模型中添加一个'role'属性，从而定义反向关系。这一 \
    # 属性可替代role_id访问Role模型，此时获取的是模型对象，而不是外键的值。
    users = db.relationship('User', backref='role', lazy='dynamic')

    # 注意这个'__repr__()'方法，常与'__str__()'方法比较
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # 'index'设置为True，将为此列创建索引，提升查询效率。
    username = db.Column(db.String(64), unique=True, index=True)
    # 'role_id'列被定义为外键，传给db.ForeignKey()的参数'roles.id'表明 \
    # 此列的值是'roles'表中行的id值。
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/', methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           form = form, name = session.get('name'),
                           known = session.get('known', False))

    #     old_name = session.get('name')
    #     if old_name is not None and old_name != form.name.data:
    #         flash('Looks like you have changed your name!')
    #     # post方法重定向get方法
    #     session['name'] = form.name.data
    #     return redirect(url_for('index'))
    # return render_template("index.html",form=form, name=session.get('name'),
    #                        current_time=datetime.utcnow())
                            # name信息被保存在session中，session跟普通字典一样，
                            # 对于不存在的键，get()会返回默认值None。


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", username=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

if __name__ == "__main__":
    app.debug = True
    manager.add_command("shell", Shell(make_context=make_shell_context))
    manager.run()
