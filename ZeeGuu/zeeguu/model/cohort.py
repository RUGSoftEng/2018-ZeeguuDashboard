import zeeguu
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from zeeguu.model.language import Language

db = zeeguu.db


class Cohort(zeeguu.db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    inv_code = db.Column(db.String(255), unique=True)
    class_name = db.Column(db.String(255))
    class_language_id = db.Column(db.Integer, db.ForeignKey(Language.id))
    max_students = db.Column(db.Integer)
    cur_students = db.Column(db.Integer)

    class_language = relationship(Language, foreign_keys=[class_language_id])

    def __init__(self,inv_code, class_name, class_language, max_students):
        self.inv_code = inv_code
        self.class_name = class_name
        self.class_language = class_language
        self.max_students = max_students
        self.cur_students = 0



    @classmethod
    def find(cls, id):
        return cls.query.filter_by(id=id).one()


    @classmethod
    def get_id(cls,inv):
        c = cls.query.filter_by(inv_code=inv).one()
        return c.id

    def request_join(self):
        if(self.cur_students<self.max_students):
            self.cur_students = self.cur_students+1
            return True
        return False

    def undo_join(self):
        if(self.cur_students > 0):
            self.cur_students = self.cur_students-1

    def get_students(self):
        from zeeguu.model.user import User

        # compatibility reasons: if there is an associated invitation code
        # use it; otherwise fallback on the cohort that's associated with the User
        if self.id:
            zeeguu.log("we have an id...")
            return User.query.filter_by(cohort_id=self.id).all()

        zeeguu.log("falling back on filtering based on cohort")
        return User.query.filter(User.cohort == self).all()

    def get_teachers(self):
        from zeeguu.model.teacher_cohort_map import TeacherCohortMap
        return TeacherCohortMap.get_teachers_for(self)

