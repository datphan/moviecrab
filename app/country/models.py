from datetime import datetime

from ..extensions import db

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(4), nullable=False, unique=True)

    @staticmethod
    def insert_countries():
        _list = [
            {'name': 'Asia', 'code': 'asia'},
            {'name': 'France', 'code': 'fr'},
            {'name': 'International', 'code': 'it'},
            {'name': 'Taiwan', 'code': 'tw'},
            {'name': 'United States', 'code': 'us'},
            {'name': 'China', 'code': 'cn'},
            {'name': 'Hongkong', 'code': 'hk'},
            {'name': 'Hongkong', 'code': 'hk'},
            {'name': 'Japan', 'code': 'jp'},
            {'name': 'Thailand', 'code': 'th'},
            {'name': 'Euro', 'code': 'eu'},
            {'name': 'India', 'code': 'in'},
            {'name': 'Korea', 'code': 'kr'},
            {'name': 'United Kingdom', 'code': 'uk'},
        ]

        for item in _list:
            record = Country.query.filter_by(code=item.get('code')).first()

            if record is None:
                record = Country(**item)
            
                db.session.add(record)
            
            db.session.commit()

    def __repr__(self):
        return '<Country(id="%s", name="%s")>' % (self.id, self.name)
