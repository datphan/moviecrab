from datetime import datetime

from ..extensions import db

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())

    def __repr__(self):
        return '<Genre(id="%s", name="%s")>' % (self.id, self.name)
