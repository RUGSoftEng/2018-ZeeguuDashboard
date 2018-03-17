from zeeguu.model.teacher_cohort_map import TeacherCohortMap


class Teacher:
    def __init__(self, user):
        self.user = user

    def get_cohorts(self):
        return TeacherCohortMap.get_cohorts_for(self.user)

    @classmethod
    def from_user(cls, user):
        cohort_count_of_user = len(TeacherCohortMap.get_cohorts_for(user))
        if cohort_count_of_user > 0:
            return cls(user)
        else:
            return None
