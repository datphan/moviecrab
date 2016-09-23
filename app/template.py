# -*- coding: utf-8 -*-

"""flask template"""

__all__ = ['init_template']

from .extensions import genre_datastore, country_datastore, movie_qualities
from datetime import date

def init_template(app):

    def has_item(item, list):
            pass

    @app.context_processor
    def inject_data():
        return dict(
                genres=genre_datastore.find_genre_list(),
                countries=country_datastore.find_country_list(),
                qualities=movie_qualities,
                has_item=has_item,
                current_year=date.today().year
            )