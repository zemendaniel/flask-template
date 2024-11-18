from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField, StringField, PasswordField, HiddenField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, length, EqualTo
from persistence.model.user import roles


class RegisterUserForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), length(max=32)])
    password = PasswordField('Password', validators=[DataRequired(), length(max=32, min=4)])
    password_again = PasswordField('Password again', validators=[DataRequired(), length(max=32, min=4), EqualTo('password')])


class EditUserRoleForm(FlaskForm):
    role = SelectField('Role', choices=[(role, roles[role]) for role in roles.keys() if role != 'super_admin'], validators=[DataRequired()])
    user_id = HiddenField('user_id', validators=[DataRequired()])

    def set_role(self, role_name):
        self.role.data = role_name

    def set_user_id(self, user_id):
        self.user_id.data = user_id


class UserSettingsForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), length(max=32)])


class UserPasswordResetForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(), length(max=32, min=4)])
    new_password_again = PasswordField('New password again', validators=[DataRequired(), length(max=32, min=4),
                                                                     EqualTo('new_password')])


class DeleteUserForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), length(max=32, min=4)])
