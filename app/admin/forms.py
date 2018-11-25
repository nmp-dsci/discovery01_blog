from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Post

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class EditPost(FlaskForm):
    title = StringField('Title of post',validators=[Required()])
    category = SelectField('Category',validators=[Required()])
    body = TextAreaField('Update post',validators=[Required()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(EditPost, self).__init__(*args, **kwargs)
        self.category.choices = [(x.category,x.category) for x in Post.query.group_by(Post.category)]
