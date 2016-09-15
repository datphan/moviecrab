# -*- coding: utf-8 -*-

"""main views"""

from flask import render_template

from flask.ext.classy import FlaskView


class GenreView(FlaskView):
    # route_base = '/genre'

    def index(self):
        return render_template('genre/list.html',)

    def get(self, name):
        return render_template('genre/index.html',
            genre=movie_datastore.read_movie(name))


