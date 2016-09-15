from datetime import datetime

from ..extensions import db

from sqlalchemy_utils import ChoiceType

class People(db.Model):
    TYPES = [
        (u'actor', u'Actor'),
        (u'director', u'Director'),
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())
    type = db.Column(ChoiceType(TYPES), nullable=False)

    def __repr__(self):
        return '<People(id="%s", name="%s")>' % (self.id, self.name)
