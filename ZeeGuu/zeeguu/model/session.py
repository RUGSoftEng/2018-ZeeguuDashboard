import datetime
import random

import zeeguu
from sqlalchemy import desc

from zeeguu.model.user import User

db = zeeguu.db


class Session(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
    last_use = db.Column(db.DateTime)

    def __init__(self, user, id_):
        self.id = id_
        self.user = user
        self.update_use_date()

    def update_use_date(self):
        self.last_use = datetime.datetime.now()

    @classmethod
    def for_user(cls, user):
        while True:
            id_ = random.randint(0, zeeguu.app.config.get("MAX_SESSION"))
            if cls.query.get(id_) is None:
                break
        return cls(user, id_)

    @classmethod
    def find_for_id(cls, session_id):
        try:
            return cls.query.filter(cls.id == session_id).one()
        except:
            return None

    # @classmethod
    # def find_for_user(cls, user):
    #     return cls.query.filter(cls.user == user).order_by(desc(cls.last_use)).first()

    @classmethod
    def find_for_user(cls, user):
        s = cls.query.filter(cls.user == user).\
            filter(cls.id < zeeguu.app.config.get("MAX_SESSION")).\
            order_by(desc(cls.last_use)).first()
        if not s:
            s = cls.for_user(user)
        return s
