# -*- coding: utf-8 -*-

"""main views"""

from flask import render_template

from flask.ext.classy import FlaskView

from ..extensions import movie_datastore, genre_datastore


class GenreView(FlaskView):
    # route_base = '/genre'

    def index(self):
        return render_template('genre/list.html',)

    def get(self, code):
        genre = genre_datastore.filter_by(code=code).first()

        return render_template('genre/index.html',
            movie_list=genre.movies,
            genre=genre)


