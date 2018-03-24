from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class CreateCohort(FlaskForm):
    class_name = StringField('Class room name', validators=[DataRequired()])
    inv_code = StringField('Invite code')
    class_language_id = StringField('Language', validators=[DataRequired()])
    max_students = StringField('Max students', validators=[DataRequired()])
    submit = SubmitField('Create classroom')