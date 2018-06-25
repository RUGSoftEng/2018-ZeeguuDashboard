from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from zeeguu_teacher_dashboard.util.classroom import verify_invite_code_exists


class EditCohort(FlaskForm):
    """
    This class extends FlaskForm. It is used when editing class information.
    """
    class_name = StringField('Class room name', validators=[DataRequired()])
    inv_code = StringField('Invite code')
    max_students = StringField('Max students', validators=[DataRequired()])
    submit = SubmitField('Create classroom')
    old_inv_code = None

    def validate(self):
        """
        This function validates the EditCohort form.
        It extends from the normal validation as we need to validate whether some
        filled in data is already in use (the class invite code).
        :return: Returns a boolean, indicating whether the form is properly filled out or not.
        """
        if not FlaskForm.validate(self):
            return False
        if verify_invite_code_exists(self.inv_code.data) and not (self.inv_code.data == self.old_inv_code):
            tmp = list(self.inv_code.errors)
            tmp.append("Code already in use!")
            self.inv_code.errors = tuple(tmp)
            return False
        return True
    def __init__(self, old_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_inv_code = old_code
