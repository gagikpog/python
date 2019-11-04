from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo #проверяет, что бы поле не было отправлено пустым
from app.models import User
from wtforms.validators import ValidationError
import re
from app.utility.utility import check_hash_password

class LoginForm(FlaskForm): #отдает поля формы в HTML
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    def validate_password(self, password):
        username = self.username.data
        curPass = password.data
        user = User.query.filter_by(username=username).first()
        print(user)
        if not user or not check_hash_password(curPass, user.password_hash):
            raise ValidationError('Неверный логин или пароль')




class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Этот логин уже занят!')

    def validate_email(self, email):
        user = User.query.filter_by(mail=email.data).first()
        if user is not None:
            raise ValidationError('Пользователь с этой почтой уже зарегистрирован!')
        
    def validate_password(self, password):
        newPassword = password.data
        pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%*^&+~:,;\-\!\\\/\.\?=]).*$"
        result = re.findall(pattern, newPassword)
        print(newPassword)
        print(result)
        if not result:
            raise ValidationError("""
                Пароль должен состоять от 8 символов, цифр и букв английского алфавита.
                Пожалуйста, введите другой пароль.
                """)