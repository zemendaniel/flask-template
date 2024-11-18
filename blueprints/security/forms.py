from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired, length


class LoginForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), length(min=1, max=32)])
    password = PasswordField('Password', validators=[DataRequired(), length(min=4, max=32)])
    stay_logged_in = BooleanField('Stay logged in for 30 days?', default=True)
