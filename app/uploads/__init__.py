# -*- coding: utf-8 -*-

"""main blueprint"""

from flask import Blueprint

__all__ = ['uploads_bp']

uploads_bp = Blueprint('uploads', __name__, static_folder='static', url_prefix='/uploads')
