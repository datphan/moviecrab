# -*- coding: utf-8 -*-

"""flask blueprints"""

from .main import main_bp
from .movie import movie_bp
from .uploads import uploads_bp
from .api_1_0 import api_bp as api_1_0_bp

__all__ = ['register_blueprints']


def register_blueprints(app):
    """register blueprints"""
    app.register_blueprint(main_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(api_1_0_bp)

    app.register_blueprint(uploads_bp)
