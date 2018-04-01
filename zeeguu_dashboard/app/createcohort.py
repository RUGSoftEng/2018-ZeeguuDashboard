from flask_wtf import FlaskForm, validators
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app.util import verify_invite_code_exists


class CreateCohort(FlaskForm):
    class_name = StringField('Class room name', validators=[DataRequired()])
    inv_code = StringField('Invite code', validators=[DataRequired()])
    class_language_id = StringField('Language', validators=[DataRequired()])
    max_students = StringField('Max students', validators=[DataRequired()])
    submit = SubmitField('Create classroom')

    def validate(self):
        if verify_invite_code_exists(self.inv_code.data):
            tmp = list(self.inv_code.errors)
            tmp.append("Code already in use!")
            self.inv_code.errors = tuple(tmp)
            return False
        return True


class EditCohort(FlaskForm):
    class_name = StringField('Class room name', validators=[DataRequired()])
    inv_code = StringField('Invite code')
    max_students = StringField('Max students', validators=[DataRequired()])
    submit = SubmitField('Create classroom')

