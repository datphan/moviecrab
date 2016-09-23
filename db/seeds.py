"""
use this command to run this file:

$ python manage.py db seed
"""

from app.auth.models import Role
from app.genre.models import Genre
from app.country.models import Country
from app.movie.models import Server


def run():
    Role.insert_roles()
    Genre.insert_genres()
    Country.insert_countries()
    Server.insert_servers()

