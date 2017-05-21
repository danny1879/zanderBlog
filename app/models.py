# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''
from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from markdown import markdown
import bleach


# 导航表
class Menus(db.Model):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    menucategory = db.relationship('Category', backref='menus', lazy='dynamic')
    menuName = db.Column(db.String(24), unique=True, index=True, nullable=False)
    orderNo = db.Column(db.Integer)
    visible = db.Column(db.Boolean, default=False)

    def to_json(self):
        json_menu = {
            'id': self.id,
            'menuname': self.menuName,
            'visibled': self.visible
        }
        return json_menu

    # 上移导航位置
    @staticmethod
    def up_menus(menu_id):
        upmenu = Menus.query.filter_by(menu_id).first()
        if upmenu is not None:
            pass

        # 插入测试数据

    @staticmethod
    def insert_test_menus():
        menuslst = [
            '学习',
            '生活',
            '随笔'
        ]
        for title in menuslst:
            menu = Menus(menuName=title)
            db.session.add(menu)
            db.session.commit()
            menu.orderNo = menu.id
            db.session.add(menu)
            db.session.commit()

        # 新增导航菜单

    @staticmethod
    def insert_menus(menuname):
        tempmenu = Menus.query.filter_by(menuName=menuname).first()
        if tempmenu is not None:
            return False
        else:
            menu = Menus(menuName=menuname)
            db.session.add(menu)
            db.session.commit()
            menu.orderNo = menu.id
            db.session.add(menu)
            db.session.commit()
            return True


# 分类表
class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    type = db.relationship('Post',backref='posttype',lazy='dynamic')
    menuid = db.Column(db.Integer, db.ForeignKey('menus.id'))
    categoryName = db.Column(db.String(32), unique=True, index=True)
    orderNo = db.Column(db.Integer)
    visibled = db.Column(db.Boolean, default=False)

    def to_json(self):
        json_category = {
            "id": self.id,
            "categoryname": self.categoryName,
            "menuid": self.menuid
        }
        return json_category

    # 新增分类
    @staticmethod
    def insert_category(categoryname, id=None,visibled=False):
        tempcategory = Category.query.filter_by(
            categoryName=categoryname).first()
        if tempcategory is not None:
            return False
        else:
            category = Category(categoryName=categoryname, menuid=id,visibled=visibled)
            db.session.add(category)
            db.session.commit()
            category.orderNo = category.id
            db.session.add(category)
            db.session.commit()
            return True

# 文章表
class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(32),unique=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    visibled = db.Column(db.Boolean,default=False)

    def to_json(self):
        json_post = {
            "id" : self.id,
            "title" : self.title,
            "body" : self.body
        }
        return json_post

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allowed_tags = ['a','abbr','acronym','b','blockquote','code',
                        'em','i','li','ol','pre','strong','ul',
                        'h1','h2','h3','p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value,output_format='html'),tags=allowed_tags,strip=True))

db.event.listen(Post.body,'set',Post.on_changed_body)


# 用户表
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    userName = db.Column(db.String(32))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError(u'该属性只读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 插入用户数据
    @staticmethod
    def insert_user():
        user = User(userName='admin', email='admin@admin.com', password='admin')
        db.session.add(user)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
