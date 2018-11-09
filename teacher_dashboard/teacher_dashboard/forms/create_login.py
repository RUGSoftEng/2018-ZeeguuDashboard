from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateLogin(FlaskForm):
    """
    This class extends FlaskForm. It is used for filling out information when logging in.
    """
    email = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('Login')
