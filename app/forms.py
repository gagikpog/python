from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo #проверяет, что бы поле не было отправлено пустым
from app.models import User
from wtforms.validators import ValidationError
import re
from app.utility.utility import check_hash_password
from flask_login import login_user

class LoginForm(FlaskForm):
    #Валидация полученных данных
    username = StringField('Телефон или почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    def validate_password(self, password):
        username = self.username.data
        curPass = password.data
        user = None
        if '@' in username:
            user = User.query.filter_by(mail=username).first()
        else:
            user = User.query.filter_by(phone=username).first()
        if not user or not check_hash_password(curPass, user.password):
            raise ValidationError('Неверный логин или пароль')
        else:
            login_user(user)




class RegistrationForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    sname = StringField('Фамилия', validators=[DataRequired()])
    pname = StringField('Отчество', validators=[DataRequired()])
    username = StringField('Телефон или почта', validators=[DataRequired()])
    activity = RadioField('Деятельность',
        choices=[('Студент', 'Студент'), ('Заказчик', 'Заказчик')], default='Студент'
    )
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторно введите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        uname = username.data
        mailPattern = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
        phonePattern = "^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$"
        if re.findall(mailPattern, uname):
            user = User.query.filter_by(mail=uname).first()
            if user is not None:
                raise ValidationError('Пользователь с этой почтой уже зарегистрирован!')
        elif re.findall(phonePattern, uname):
            user = User.query.filter_by(phone=uname).first()
            if user is not None:
                raise ValidationError('Пользователь с таким номером телефона уже зарегистрирован!')
        else:
            raise ValidationError('Некорректный логин!')


    def validate_password(self, password):
        newPassword = password.data
        passPattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%*^&+~:,;\-\!\\\/\.\?=]).*$"
        result = re.findall(passPattern, newPassword)
        if not result:
            raise ValidationError("""
                Пароль должен состоять от 8 символов, цифр и букв английского алфавита.
                Пожалуйста, введите другой пароль.
                """)
