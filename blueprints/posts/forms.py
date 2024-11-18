from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
