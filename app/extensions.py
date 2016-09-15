# -*- coding: utf-8 -*-

"""flask extensions"""

from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore, Security
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from flask_cors import CORS
from flask_jwt import JWT
from flask_bower import Bower

from .auth.datastore import SQLAlchemyAuthDatastore
from .movie.datastore import SQLAlchemyMovieDatastore
from .genre.datastore import SQLAlchemyGenreDatastore
from .people.datastore import SQLAlchemyPeopleDatastore
from .tag.datastore import SQLAlchemyTagDatastore


__all__ = ['init_apps', 'heroku', 'db', 'migrate', 'mail', 'auth_datastore']

heroku = Heroku()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
security = Security()
cors = CORS()
jwt = JWT()

# models must be imported before datastore initialization
from .auth.models import User, Role
from .people.models import People
from .movie.models import Server, Movie, Episode, Source
from .genre.models import Genre
from .tag.models import Tag
from .country.models import Country

auth_datastore = SQLAlchemyAuthDatastore(db)

movie_datastore = SQLAlchemyMovieDatastore(db)

genre_datastore = SQLAlchemyGenreDatastore(db)

people_datastore = SQLAlchemyPeopleDatastore(db)

tag_datastore = SQLAlchemyTagDatastore(db)


def init_apps(app):
    if app.config['DEBUG'] and not app.config['TESTING']:
        from flask_debugtoolbar import DebugToolbarExtension

        DebugToolbarExtension(app)

    @app.context_processor
    def inject_user():
        return dict(
                genres=genre_datastore.find_genre_list(),
            )

    from .movie.admin import MovieAdminView, MovieEpisodeAdminView
    from .people.admin import PeopleAdminView

    from .main.views import MainView
    from .movie.views import MovieView
    from .genre.views import GenreView
    from .tag.views import TagView

    Bower(app)

    heroku.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role))
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    jwt.init_app(app)

    admin = Admin(name='flask-boilerplate')
    # add admin model views

    admin.add_view(ModelView(User, db.session, category='Users'))
    admin.add_view(ModelView(Role, db.session, category='Users'))
    admin.add_view(MovieAdminView(Movie, db.session, category='Movies'))
    admin.add_view(MovieEpisodeAdminView(Episode, db.session, category='Movie sources'))
    admin.add_view(ModelView(Genre, db.session, category='Movies'))
    admin.add_view(ModelView(Tag, db.session, category='Movies'))
    admin.add_view(ModelView(Server, db.session, category='Movies'))
    admin.add_view(PeopleAdminView(People, db.session, category='Movies'))

    admin.init_app(app)

    MainView.register(app)
    MovieView.register(app)
    GenreView.register(app)
    TagView.register(app)
