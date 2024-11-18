from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileSize
from wtforms.fields.simple import TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Optional


class SetOrgNameForm(FlaskForm):
    name = TextAreaField("Név", validators=[DataRequired(), Length(max=255)])


class SetFaviconForm(FlaskForm):
    icon = FileField("Favicon - maximum 1 MB, ico and png files only", validators=[
        FileRequired(),
        FileAllowed(['ico', 'png']),
        FileSize(max_size=1024 * 1024)
    ])


class SetWelcomeTextForm(FlaskForm):
    text = TextAreaField("Text", validators=[Length(max=5000)])
