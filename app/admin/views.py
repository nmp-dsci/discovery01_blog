from flask import render_template, url_for
from . import admin


@admin.route('/')
def admin_home():
    return render_template('admin/admin_home.html')

@admin.route('/login')
def login():
    return render_template('admin/login.html')


@admin.route('/profile')
def profile():
    return render_template('admin/profile.html')


@admin.route('/create')
def create():
    return render_template('admin/create.html')