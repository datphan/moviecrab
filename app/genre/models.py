from datetime import datetime

from ..extensions import db

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.Text())

    @staticmethod
    def insert_genres():
        _list = [
            {'name': 'Fantasy', 'code': 'fantasy'},
            {'name': 'War', 'code': 'war'},
            {'name': 'Violen & Gore', 'code': 'violen_gore'},
            {'name': 'Adventure', 'code': 'adventure'},
            {'name': 'Fiction', 'code': 'fiction'},
        ]

        for item in _list:
            record = Genre.query.filter_by(code=item.get('code')).first()

            if record is None:
                record = Genre(**item)

                db.session.add(record)

            db.session.commit()

    def __repr__(self):
        return '<Genre(id="%s", name="%s")>' % (self.id, self.name)
