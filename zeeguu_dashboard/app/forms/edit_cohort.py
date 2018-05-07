from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EditCohort(FlaskForm):
    """
    This class extends FlaskForm. It is used when editing class information.
    """
    class_name = StringField('Class room name', validators=[DataRequired()])
    inv_code = StringField('Invite code')
    max_students = StringField('Max students', validators=[DataRequired()])
    submit = SubmitField('Create classroom')
