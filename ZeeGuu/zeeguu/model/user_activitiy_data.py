from datetime import datetime
import zeeguu

from zeeguu.model.user import User
from zeeguu.constants import JSON_TIME_FORMAT

db = zeeguu.db


class UserActivityData(db.Model):
    __table_args__ = dict(mysql_collate="utf8_bin")
    __tablename__ = 'user_activity_data'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

    time = db.Column(db.DateTime)

    event = db.Column(db.String(255))
    value = db.Column(db.String(255))
    extra_data = db.Column(db.String(4096))

    def __init__(self, user, time, event, value, extra_data):
        self.user = user
        self.time = time
        self.event = event
        self.value = value
        self.extra_data = extra_data

    def data_as_dictionary(self):
        return dict(
            user_id=self.user_id,
            time=self.time.strftime("%Y-%m-%dT%H:%M:%S"),
            event=self.event,
            value=self.value,
            extra_data=self.extra_data
        )

    def _extra_data_filter(self, attribute_name: str):
        """
            required by .find()
            used to parse extra_data to find a specific attribute

            example of extra_data:

                 {"80":[{"title":"Tour de France - Pourquoi n'ont-ils pas attaqué Froome après son tout-droit","url":"https://www.lequipe.fr/Cyclisme-sur-route/Actualites/Pourquoi-n-ont-ils-pas-attaque-froome-apres-son-tout-droit/818035#xtor=RSS-1","content":"","summary"…

        :param attribute_name -- e.g. "title" in the above exaxmple
        :return: value of attribute
        """
        start = str(self.extra_data).find("\"" + attribute_name + "\":") + len(attribute_name) + 4
        end = str(self.extra_data)[start:].find("\"")
        return str(self.extra_data)[start:end + start]

    @classmethod
    def _filter_by_extra_value(cls, events, extra_filter, extra_value):
        """

            required by .find()

        :param events:
        :param extra_filter:
        :param extra_value:
        :return:
        """
        filtered_results = []

        for event in events:
            extradata_value = event._extra_data_filter(extra_filter)
            if extradata_value == extra_value:
                filtered_results.append(event)
        return filtered_results

    @classmethod
    def find(cls,
             user: User = None,
             extra_filter: str = None,
             extra_value: str = None,
             event_filter: str = None,
             only_latest=False):
        """

            Find one or more user_activity_data by any of the above filters

        :return: object or None if not found
        """
        query = cls.query
        if event_filter is not None:
            query = query.filter(cls.event == event_filter)
        if user is not None:
            query = query.filter(cls.user == user)
        query = query.order_by('time')

        try:
            events = query.all()
            if extra_filter is None or extra_value is None:
                if only_latest:
                    return events[0]
                else:
                    return events

            filtered = cls._filter_by_extra_value(events, extra_filter, extra_value)
            if only_latest:
                return filtered[0]
            else:
                return filtered
        except:
            return None

    @classmethod
    def create_from_post_data(cls, session, data, user):
        time = data['time']
        event = data['event']
        value = data['value']
        extra_data = data['extra_data']

        zeeguu.log(f'{event} value[:42]: {value[:42]} extra_data[:42]: {extra_data[:42]}')

        new_entry = UserActivityData(user,
                                     datetime.strptime(time, JSON_TIME_FORMAT),
                                     event,
                                     value,
                                     extra_data)
        session.add(new_entry)
        session.commit()
