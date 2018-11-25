from flask import render_template, url_for,redirect,request,flash
from . import admin
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User, Post
from .forms import LoginForm,EditPost
from datetime import datetime

@admin.route('/',methods=['GET'])
@login_required
def admin_home():
    columns = {'id':'post ID','category':'category',
    'create_timestamp':'create time','edit_timestamp':'last edited',
    'title':'title','edit':'edit'}
    data = Post.query.filter_by(author_id = current_user.id).order_by(Post.edit_timestamp.desc())
    return render_template('admin/admin_home.html',columns=columns,table = data)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.home'))
        flash('Invalid username or password.')
    return render_template('admin/login.html', form=form)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))


@admin.route('/profile')
@login_required
def profile():
    return render_template('admin/profile.html')


@admin.route('/create')
@login_required
def create_post():
    return render_template('admin/create_post.html')


@admin.route('/edit-post/<int:id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    form = EditPost()
    post = Post.query.filter_by(id = id).first()
    if post is not None:
        if form.validate_on_submit():
            post.title = form.title.data
            post.category = form.category.data
            post.body = form.body.data
            post.edit_timestamp = datetime.utcnow()
            db.session.add(post)
            flash('Blog titled "%s" has been updated.' % (post.title))
            return redirect(url_for('main.blog',id=id))
        form.title.data = post.title
        form.category.data = post.category
        form.body.data = post.body
        return render_template('admin/edit_post.html', id = id, form=form)
    else: 
            flash("Can't find blog for ID provided: %d" % (id))
            return redirect(url_for('main.home'))

