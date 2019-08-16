from flask_wtf import Form
from wtforms import (StringField, DateField, IntegerField, TextField
                        , TextAreaField, PasswordField)
from wtforms.validators import DataRequired, EqualTo

from models import Journal

class JournalForm(Form):
    title = StringField('title', validators=[DataRequired()])

    date = DateField('date', validators=[DataRequired()])

    time_spent = IntegerField('time_spent', validators=[DataRequired()])

    what_you_lean = TextAreaField('what_you_lean', validators=[DataRequired()])

    resource_to_remember = TextAreaField('resource_to_remember',
        validators=[DataRequired()])
    tag = TextField('tag', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField(
        'password',
        validators=[DataRequired(),
        EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField('check password', validators=[DataRequired()])



class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
