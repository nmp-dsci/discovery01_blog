from flask import render_template, url_for,redirect,request,flash
from . import admin
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User
from .forms import LoginForm

@admin.route('/',methods=['GET'])
@login_required
def admin_home():
    return render_template('admin/admin_home.html')

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

