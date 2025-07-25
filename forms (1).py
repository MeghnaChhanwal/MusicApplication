from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, ValidationError

class RegisterForm(FlaskForm):
    UserName = StringField('Username:', validators=[DataRequired(), Length(min=2, max=10)])
    Password = PasswordField('Password:', validators=[DataRequired()])
    ConfirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password')])
    Age = IntegerField('Age:', validators=[DataRequired(), NumberRange(min=18, max=30, message='Age must be between 18 and 30')])
    Submit = SubmitField('Register Here!')

class LoginForm(FlaskForm):
    UserName = StringField('Username:', validators=[DataRequired()])
    Password = PasswordField('Password:', validators=[DataRequired()])
    Submit = SubmitField('Login Here!')


    