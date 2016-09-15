# -*- coding: utf-8 -*-

"""main blueprint"""

from flask import Blueprint

__all__ = ['tag_bp']

tag_bp = Blueprint('tag', __name__)

from . import views
