from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from models import Author, User


def custom_email_checker(form, field):
    user = User.query.filter_by(mail=field.data).first()
    if user is not None:
        raise ValidationError("Mail istifadededir")
    
    if field.data.endswith("mail.ru"):
        raise ValidationError("Mail blacklistdedir")



class RegisterForm(FlaskForm):
    name = StringField("Adinizi daxil edin", validators=[DataRequired(), Length(min=5, max=20)])
    surname = StringField("Soyadinizi daxil edin", validators=[DataRequired()])
    mail = EmailField("Email daxil edin", validators=[DataRequired(), custom_email_checker])
    password = PasswordField("Sifre", validators=[DataRequired()])
    confirm_password = PasswordField("Sifrenin tekrari", validators=[DataRequired(), EqualTo("password",
                                                                                             message="Sifreler uygun gelmir")])


    submit= SubmitField("Qeydiyyat")


class LoginForm(FlaskForm):
    mail = EmailField("Email daxil edin", validators=[DataRequired()])
    password = PasswordField("Sifre", validators=[DataRequired()])

    submit = SubmitField("Daxil ol") 