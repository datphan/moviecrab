# -*- coding: utf-8 -*-

"""main views"""

from flask import render_template, request

from ..extensions import movie_datastore

from flask.ext.classy import FlaskView, route

from ..pagination import OffsetPagination
    

class MovieView(FlaskView):
    # route_base = '/movie'

    def index(self):
        pagination = OffsetPagination(movie_datastore.find_movie_list())

        return render_template('movie/list.html',
            filter_type='lastest',
            pagination=pagination,
            movie_list=pagination.data)

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

    def filter(self, type):
        pagination = OffsetPagination(movie_datastore.find_movie_list(),
                        limit=int(request.args.get('limit') or 10),
                        offset=int(request.args.get('offset') or 0))

        return render_template('movie/filter.html',
            filter_type=type,
            filter_category=request.args.get('category'),
            filter_genres=request.args.get('genres'),
            filter_countries=request.args.get('countries'),
            filter_quality=request.args.get('quality'),
            filter_year=request.args.get('year'),
            pagination=pagination,
            movie_list=pagination.data)

