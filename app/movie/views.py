# -*- coding: utf-8 -*-

"""main views"""

from flask import render_template

from ..extensions import movie_datastore

from flask.ext.classy import FlaskView




class MovieView(FlaskView):
    # route_base = '/movie'

    def index(self):
        return render_template('movie/list.html',)

    def get(self, id):
        movie = movie_datastore.read_movie(id)

        movie_list_related = movie_datastore.find_movie_list(filters=[
                    ('type', 'eq', movie.type),
                    ('id', 'ne', movie.id),
                ])

        return render_template('movie/index.html',
            movie_list_related = movie_list_related,
            movie = movie)

    def card(self, id):
        return render_template('movie/card.html',
            movie = movie_datastore.read_movie(id))

    def play(self, id):
        movie = movie_datastore.read_movie(id)

        movie_list_related = movie_datastore.find_movie_list(filters=[
                    ('type', 'eq', movie.type),
                    ('id', 'ne', movie.id),
                ])

        episodes = movie.episodes

        servers = dict()

        for episode in episodes:
            name = episode.server and episode.server.name or 'Default'

            if name not in servers:
                servers[name] = []

            servers[name].append(episode)

        return render_template('movie/play.html',
            movie_list_related = movie_list_related,
            movie = movie,
            servers = servers)

