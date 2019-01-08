from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired
from zeeguu_teacher_dashboard.util.classroom import verify_invite_code_exists

one_to_ten = [('0', '-')] + [(str(each), str(each)) for each in range(1, 11)]


def validate_inv_code(form, field):
    """
    This function validates the EditCohort form.
    It extends from the normal validation as we need to validate whether some
    filled in data is already in use (the class invite code).
    :return: Returns a boolean, indicating whether the form is properly filled out or not.
    """
    print("trying to validate...")

    if form.inv_code.data.strip() == "":
        form.inv_code.errors.append("You must define an invite code")
        return False

    if verify_invite_code_exists(form.inv_code.data) and not (form.inv_code.data == form.old_inv_code):
        form.inv_code.errors.append("Code already in use!")
        print(form.inv_code.errors)
        return False

    print("done with the validation! returning")
    return True


class EditCohort(FlaskForm):
    """
    This class extends FlaskForm. It is used when editing class information.
    """
    name = StringField('Class name', validators=[DataRequired()])
    inv_code = StringField('Invite code', [DataRequired(), validate_inv_code])
    declared_level_min = SelectField('Min: ', choices=one_to_ten)
    declared_level_max = SelectField('Max: ', choices=one_to_ten)
    language_name = StringField('Language Name')

    old_inv_code = None

    def __init__(self, old_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_inv_code = old_code
