from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class CreateCohort(FlaskForm):
    cohort_name = StringField('Class room name', validators=[DataRequired()])
    invite_code = StringField('Invite code')
    language = StringField('Language', validators=[DataRequired()])
    teacher_id = StringField('Teacher id', validators=[DataRequired()])
    submit = SubmitField('Create classroom')