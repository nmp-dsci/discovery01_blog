from flask import render_template, url_for
from . import main
from ..models import Permission, Role, User, Post


@main.route('/',methods=['GET'])
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('main/home.html', posts=posts)

@main.route('/contact',methods=['GET'])
def contact():
    return render_template('main/contact.html')

@main.route('/about',methods=['GET'])
def about():
    return render_template('main/about.html')

@main.route('/blog/<int:id>',methods=['GET'])
def blog(id):
    return render_template('main/blog.html',id = id)
