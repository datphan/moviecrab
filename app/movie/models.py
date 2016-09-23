from datetime import datetime

from ..extensions import db, movie_qualities

from sqlalchemy_utils import ChoiceType


genres_movies = db.Table('genre_meta',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
);

actors_movies = db.Table('actor_meta',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'))
);

directors_movies = db.Table('director_meta',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'))
);

countries_movies = db.Table('country_meta',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('country_id', db.Integer, db.ForeignKey('country.id'))
);

tags = db.Table('tag_meta',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
);

class Movie(db.Model):
    QUALITIES = movie_qualities

    TYPES = [
        (u'series', u'TV Series'),
        (u'single', u'Movie'),
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text())
    quality = db.Column(ChoiceType(QUALITIES), nullable=False)
    imdb_id = db.Column(db.Integer(), nullable=False)
    duration = db.Column(db.Integer(), nullable=False)
    release = db.Column(db.DateTime(), nullable=False)
    #rating_point = db.Column(db.Float())
    type = db.Column(ChoiceType(TYPES), nullable=False)
    #visit = db.Column(db.Integer())
    poster = db.Column(db.String(500))
    thumbnail = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    episodes = db.relationship('Episode', backref='movie', lazy='dynamic')

    genres = db.relationship('Genre', secondary=genres_movies,
                            backref=db.backref('movies', lazy='dynamic'))

    actors = db.relationship('People', secondary=actors_movies,
                            backref=db.backref('acted_movies', lazy='dynamic'))

    directors = db.relationship('People', secondary=directors_movies,
                            backref=db.backref('created_movies', lazy='dynamic'))

    countries = db.relationship('Country', secondary=countries_movies,
                            backref=db.backref('movies', lazy='dynamic'))

    tags = db.relationship('Tag', secondary=tags,
                            backref=db.backref('movies', lazy='dynamic'))

    def __repr__(self):
        return '<Movie(id="%s", name="%s")>' % (self.id, self.name)

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text())
    subtitle = db.Column(db.String(500))
    duration = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))
    server = db.relationship('Server')

    sources = db.relationship('Source', backref='episode')

    def __repr__(self):
        return '<Episode(id="%s", name="%s")>' % (self.id, self.name)

class Server(db.Model):
    """docstring for Server"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text())

    @staticmethod
    def insert_servers():
        _list = [
            {'name': 'Default', 'description': 'Current server'},
            {'name': 'Google', 'description': 'Google video'},
            {'name': 'Youtube', 'description': 'Youtube'},
        ]

        for item in _list:
            record = Server.query.filter_by(name=item.get('name')).first()

            if record is None:
                record = Server(**item)

                db.session.add(record)

            db.session.commit()

    def __repr__(self):
        return '<Server(id="%s", name="%s")>' % (self.id, self.name)


class Source(db.Model):
    QUALITIES = movie_qualities

    """docstring for Source"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.String(500), nullable=False)
    quality = db.Column(ChoiceType(QUALITIES), nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'))

    def __repr__(self):
        return '<Source(id="%s", link="%s")>' % (self.id, self.link)


        
