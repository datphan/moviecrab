from datetime import datetime

from ..extensions import db

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return '<Country(id="%s", name="%s")>' % (self.id, self.name)
