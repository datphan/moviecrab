# -*- coding: utf-8 -*-

"""main views"""

from flask import render_template

from flask.ext.classy import FlaskView

from ..extensions import movie_datastore, country_datastore


class CountryView(FlaskView):
    # route_base = '/country'

    def index(self):
        return render_template('country/list.html',)

    def get(self, code):
        country = country_datastore.filter_by(code=code).first()

        return render_template('country/index.html',
            movie_list=country.movies,
            country=country)


