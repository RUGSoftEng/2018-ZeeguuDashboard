from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from zeeguu_teacher_dashboard.util.classroom import verify_invite_code_exists

from .edit_cohort import one_to_ten

"""
The create cohort form class file.
"""


class CreateCohort(FlaskForm):
    """
    This class extends from FlaskForm. It is used for the form when filling out
    the information of a new class.
    """
    name = StringField('Class room name', validators=[DataRequired()])
    inv_code = StringField('Invite code', validators=[DataRequired()])
    class_language_id = StringField('Language', validators=[DataRequired()])
    max_students = StringField('Max students', validators=[DataRequired()])
    declared_level_min = SelectField('Min: ', choices=one_to_ten)
    declared_level_max = SelectField('Max: ', choices=one_to_ten)

    submit = SubmitField('Create classroom')

    def validate(self):
        """
        This function validates the CreateCohort form.
        It extends from the normal validation as we need to validate whether some
        filled in data is already in use (the class invite code).
        :return: Returns a boolean, indicating whether the form is properly filled out or not.
        """
        if not FlaskForm.validate(self):
            return False
        if verify_invite_code_exists(self.inv_code.data):
            tmp = list(self.inv_code.errors)
            tmp.append("Code already in use!")
            self.inv_code.errors = tuple(tmp)
            return False
        return True
