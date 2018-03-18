import zeeguu

from zeeguu.model.exercise_outcome import ExerciseOutcome
from zeeguu.model.exercise_source import ExerciseSource

db = zeeguu.db


class Exercise(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    outcome_id = db.Column(db.Integer, db.ForeignKey(ExerciseOutcome.id), nullable=False)
    outcome = db.relationship(ExerciseOutcome)
    source_id = db.Column(db.Integer, db.ForeignKey(ExerciseSource.id), nullable=False)
    source = db.relationship(ExerciseSource)
    solving_speed = db.Column(db.Integer)
    time = db.Column(db.DateTime, nullable=False)

    def __init__(self, outcome, source, solving_speed, time):
        self.outcome = outcome
        self.source = source
        self.solving_speed = solving_speed
        self.time = time

    def short_string_summary(self):
        return str(self.source.id) + self.outcome.outcome[0]

    def __str__(self):
        return f'{self.source.source} ' + str(self.time) + f' {self.outcome.outcome}'
