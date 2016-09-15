# -*- coding: utf-8 -*-

"""main views"""

from flask import render_template

from flask.ext.classy import FlaskView


class TagView(FlaskView):
    # route_base = '/tag'

    def index(self):
        return render_template('tag/list.html',)

    def get(self, name):
        return render_template('tag/index.html',)


