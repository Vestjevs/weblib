from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField

from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])


class RegistrationForm(Form):
    username = StringField('Логин', validators=[DataRequired()])
    password_one = PasswordField('Пароль', validators=[DataRequired()])
    password_two = PasswordField('Пароль еще раз', validators=[DataRequired()])


class BookForm(Form):
    title = TextAreaField('Название', validators=[DataRequired()])
    abstract = TextAreaField('Аннотация', validators=[DataRequired()])


class AuthorForm(Form):
    name = TextAreaField('Имя', validators=[DataRequired()])


class SearchForm(Form):
    query = TextAreaField('Поиск', validators=[DataRequired()])
