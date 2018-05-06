from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app.util.classroom import verify_invite_code_exists

"""
The create cohort form class file.
"""

class CreateCohort(FlaskForm):
    """
    This class extends from FlaskForm. It is used for the form when filling out
    the information of a new class.
    """
    class_name = StringField('Class room name', validators=[DataRequired()])
    inv_code = StringField('Invite code', validators=[DataRequired()])
    class_language_id = StringField('Language', validators=[DataRequired()])
    max_students = StringField('Max students', validators=[DataRequired()])
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