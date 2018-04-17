from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class CreateLogin(FlaskForm):
    email = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

    submit = SubmitField('Create classroom')