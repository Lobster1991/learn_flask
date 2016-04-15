# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__) # <Flask 'hello'>

db = SQLAlchemy(app)



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
