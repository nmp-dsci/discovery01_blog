import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
import os, random

# use these to define what a user can do
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class PostCategories:
    categories =    [   
            'World'
        ,   'Technology'
        ,   'Design'
        ,   'Culture'
        ,   'Business'
        ,   'Politics'
        ,   'Opinion'
        ,   'Science'
        ,   'Health'
        ,   'Style'
        ,   'Travel'
        ]

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            # 'User': (Permission.FOLLOW |
            #          Permission.COMMENT |
            #          Permission.WRITE_ARTICLES, True),
            # 'Moderator': (Permission.FOLLOW |
            #               Permission.COMMENT |
            #               Permission.WRITE_ARTICLES |
            #               Permission.MODERATE_COMMENTS, False),
            'Admin': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name



# 20181121: only "ADMIN" user for now
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    # confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    # avatar_hash = db.Column(db.String(32))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @staticmethod
    def generate_demo(count=1):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        u = User(email=os.environ.get('DISCOVERY01_ADMIN')
            ,   username='demo_admin'
            ,   password='demo_demo'
            #,   confirmed=True
            ,   name=forgery_py.name.full_name()
            ,   location=forgery_py.address.city()
            ,   about_me=forgery_py.lorem_ipsum.sentence()
            ,   member_since=forgery_py.date.date(True)
            )
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['DISCOVERY01_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        # if self.email is not None and self.avatar_hash is None:
        #     self.avatar_hash = hashlib.md5(
        #         self.email.encode('utf-8')).hexdigest()
        # self.followed.append(Follow(followed=self))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category = db.Column(db.Text)
    # comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def generate_demo(count=50):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(
                    title=forgery_py.lorem_ipsum.title()
                ,   body=forgery_py.lorem_ipsum.sentences(randint(1, 5))
                ,   timestamp=forgery_py.date.date(True,0,600)
                ,   author=u
                ,   category=random.sample(PostCategories.categories,k=1)[0]
                )
            db.session.add(p)
            db.session.commit()



