from flask import render_template, url_for
from . import main
from ..models import Permission, Role, User, Post
from sqlalchemy import func
from .. import db


@main.route('/',methods=['GET'])
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    categories = db.session.query(Post.category, func.count(Post.id)).group_by(Post.category).order_by(func.count(Post.id).desc()).all()
    return render_template('main/home.html', posts=posts,categories=categories)

@main.route('/<category>',methods=['GET'])
def category(category):
    posts = Post.query.filter(Post.category.ilike(category)).order_by(Post.timestamp.desc()).all()
    categories = db.session.query(Post.category, func.count(Post.id)).group_by(Post.category).order_by(func.count(Post.id).desc()).all()
    return render_template('main/home.html', posts=posts,categories=categories)

@main.route('/contact',methods=['GET'])
def contact():
    return render_template('main/contact.html')

@main.route('/about',methods=['GET'])
def about():
    return render_template('main/about.html')

@main.route('/blog/<int:id>',methods=['GET'])
def blog(id):
    post = Post.query.filter_by(id = id).first()
    return render_template('main/blog.html',post = post)
