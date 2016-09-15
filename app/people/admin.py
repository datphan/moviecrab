# -*- coding: utf-8 -*-
from .models import People

from flask_admin.contrib.sqla import ModelView

from ..extensions import db

class PeopleAdminView(ModelView):
    form_choices = {
        'type': People.TYPES,
    }
