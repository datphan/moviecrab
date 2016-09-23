# -*- coding: utf-8 -*-

"""main views"""

from flask import render_template
from . import main_bp
from flask.ext.classy import FlaskView, route
from ..extensions import movie_datastore


class MainView(FlaskView):
    route_base = '/'

    def index(self):
        movie_list = movie_datastore.find_movie_list()

        movie_list_lastest = movie_datastore.find_movie_list(filters=[('type', 'eq', 'single'), ],
                sort='-movie_updated_at')

        movie_list_tv = movie_datastore.find_movie_list(filters=[('type', 'eq', 'series'), ])

        movie_list_requested = movie_datastore.find_movie_list()

        movie_list_featured = movie_datastore.find_movie_list()

        return render_template('main/home.html',
            movie_list=movie_list,
            movie_list_lastest=movie_list_lastest,
            movie_list_tv=movie_list_tv,
            movie_list_requested=movie_list_requested,
            movie_list_featured=movie_list_featured,)

    def get(self, id):
        pass


# @main_bp.route('/')
# def main():
#     """hello world view"""
#     return render_template('main/home.html')
