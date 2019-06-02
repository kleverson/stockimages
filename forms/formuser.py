from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField, SelectMultipleField, \
    widgets, ValidationError

from models.User import Role, User


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class LoginForm(FlaskForm):
    email = StringField("email", [validators.Length(min=4, max=255), validators.DataRequired(), validators.Email()])
    password = PasswordField("password", [validators.Length(min=4, max=25), validators.DataRequired()])


class LostFormPassword(FlaskForm):
    email = StringField("email", [validators.Length(min=4, max=255), validators.DataRequired(), validators.Email()])


class RecoverFormPassword(FlaskForm):
    password = PasswordField("password", [
        validators.length(min=3),
        validators.DataRequired(),
        validators.EqualTo('confirmpassword', message="A senha e a confirmação devem ser iguais")
    ])
    confirmpassword = PasswordField("confirm")


class RegisterFormUser(FlaskForm):

    name = StringField("name", [validators.Length(min=4, max=255), validators.DataRequired()])
    email = StringField("email", [validators.Length(min=4, max=255), validators.DataRequired(), validators.Email()])

    password = PasswordField("password", [
        validators.length(min=3),
        validators.DataRequired(),
        validators.EqualTo('confirmpassword', message="A senha e a confirmação devem ser iguais")
    ])
    confirmpassword = PasswordField("confirm")

    def validate_email(self, email):
        u = User.query.filter_by(email=self.email.data).first()
        if u is not None:
            raise ValidationError('Este e-mail já esta cadastrado!')


class RegisterFormAdminUser(FlaskForm):

    name = StringField("name", [validators.Length(min=4, max=255), validators.DataRequired()])
    email = StringField("email", [validators.Length(min=4, max=255), validators.DataRequired(), validators.Email()])
    password = PasswordField("password", [
        validators.length(min=3),
        validators.DataRequired(),
        validators.EqualTo('confirmpassword', message="A senha e a confirmação devem ser iguais")
    ])
    confirmpassword = PasswordField("confirm")


class EditFormAdminUser(FlaskForm):

    name = StringField("name", [validators.Length(min=4, max=255), validators.DataRequired()])
    email = StringField("email", [validators.Length(min=4, max=255), validators.DataRequired(), validators.Email()])


class ProfileFormUser(FlaskForm):

    name = StringField("name", [validators.Length(min=4, max=255), validators.DataRequired()])
    email = StringField("email", [validators.Length(min=4, max=255), validators.DataRequired(), validators.Email()])
    password = PasswordField("password", [
        validators.length(min=3),
        validators.DataRequired(),
        validators.EqualTo('confirmpassword', message="A senha e a confirmação devem ser iguais")
    ])
    confirmpassword = PasswordField("confirm")