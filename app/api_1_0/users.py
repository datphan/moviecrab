# -*- coding: utf-8 -*-

"""Users API"""

from flask import url_for
from flask_security import current_user
from flask_restful import marshal_with
from flask_restful import inputs

from ..api import (permissions_accepted, one_of, anonymous_required, auth_required, validators,
                   roles_required, BaseResource, TokenRequiredResource, token_auth_required,
                   permissions_required, make_empty_response, marshal_with_data_envelope)
from ..auth import user_permission, admin_role_permission
from ..extensions import auth_datastore
from ..api.decorators import paginated

from . import api
from .fields import user_fields, user_list_fields, user_token_fields


@api.resource('/users', endpoint='users')
class UserListAPI(BaseResource):
    action_decorators = {
        'get': [token_auth_required(), roles_required('admin')],
        # allow both anonymous users and admin to create a new user
        'post': [one_of(anonymous_required, admin_role_permission)]
    }

    def __init__(self):
        super(UserListAPI, self).__init__()

        self.add_argument('get', 'email', validators.Email())
        self.add_argument('get', 'active', inputs.boolean)

        self.add_argument('post', 'email', validators.Email(), required=True)
        self.add_argument('post', 'password', validators.password, required=True)
        self.add_argument('post', 'active', inputs.boolean)

    @marshal_with(user_list_fields)
    @paginated
    def get(self):
        args = self.parse_arguments()
        return auth_datastore.find_users(**args), args

    @marshal_with_data_envelope(user_token_fields)
    def post(self):
        """register a new user"""
        # TODO(hoatle): check the flow to have activation step
        user = auth_datastore.create_user(**self.parse_arguments())
        location = url_for('.user', _external=True, **{'user_id': user.id})
        return user, 201, {
            'Location': location
        }


@api.resource('/users/<user_id>', endpoint='user')
class UserAPI(TokenRequiredResource):

    action_decorators = {
        'get': [permissions_accepted(user_permission, admin_role_permission)],
        'put': [permissions_accepted(user_permission, admin_role_permission)],
        'delete': [permissions_required(admin_role_permission)]
    }

    def __init__(self):
        super(UserAPI, self).__init__()
        self.add_argument('put', 'active', bool, default=True, help='active or not')

    @marshal_with_data_envelope(user_fields)
    def get(self, user_id):
        """Get a specified user"""
        if user_id == 'me':
            user_id = current_user.id

        return auth_datastore.read_user(user_id, **self.parse_arguments())

    @marshal_with_data_envelope(user_fields)
    def put(self, user_id):
        """Update a specified user"""
        if 'me' == user_id:
            user_id = current_user.id

        return auth_datastore.update_user(user_id, **self.parse_arguments())

    def delete(self, user_id):
        """Delete a specified user"""
        auth_datastore.delete_user(user_id, **self.parse_arguments())
        return make_empty_response(200)