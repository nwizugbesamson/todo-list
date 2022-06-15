from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired


# registration form
class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    email = EmailField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label="Register")


# CREATE LOGIN FORM
class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label="Login")


# FORM FOR SINGLE LIST ENTRY
class EntryForm(FlaskForm):
    entry = StringField(label="Input Task", validators=[DataRequired()])
    submit = SubmitField(label="add task")


# FORM FOR SINGLE LIST EDIT
class EditForm(FlaskForm):
    entry = StringField(label="Edit Task", validators=[DataRequired()])
    submit = SubmitField(label="Edit")

# FORM FOR  LIST NAME EDIT
class ListForm(FlaskForm):
    name = StringField(label="Change Name", validators=[DataRequired()])
    submit = SubmitField(label="Edit")
