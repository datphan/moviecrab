# -*- coding: utf-8 -*-

"""main blueprint"""

from flask import Blueprint

__all__ = ['movie_bp']

movie_bp = Blueprint('movie_bp', __name__)


# from .views import MovieView

# MovieView.register(movie_bp)

