from flask_wtf import Form
from wtforms import PasswordField,IntegerField,SubmitField,StringField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo


class RegistrationForm(Form):
    userName=StringField("UserName",validators=[DataRequired(),Length(min=2,max=20)])
    emailId=StringField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired(),Length(min=8)])
    confirm_password=PasswordField("Confirm_Password",validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

class LoginForm(Form):
    emailId=StringField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    remember=BooleanField("remember me")
    submit=SubmitField('Login')


