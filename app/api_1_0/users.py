from flask import url_for
from flask_security import current_user
from flask_classy import route
from webargs import Arg
from webargs.flaskparser import use_args

from ..auth import admin_role_permission, user_permission
from ..api import (Resource, marshal_with, marshal_with_data_envelope, token_auth_required, one_of,
                   anonymous_required, permissions_required, validators, paginated, extract_args)
from ..api.args import BoolArg
from ..extensions import auth_datastore
from ..exceptions import UnauthorizedException

from .schemas import UserSchema, UserListSchema, RoleListSchema
from .args import user_args

_user_schema = UserSchema()
_user_list_schema = UserListSchema()
_role_list_schema = RoleListSchema()


search_args = {
    'email': Arg(str, validate=validators.Email()),
    'active': BoolArg
}


class UserResource(Resource):

    @staticmethod
    def _check_current_user_or_admin_role(user_id):
        if 'me' == user_id:
            user_id = current_user.id

        specified_user_permission = user_permission(long(user_id))

        if not (specified_user_permission.can() or admin_role_permission.can()):
            description = '{} or {} required'.format(specified_user_permission,
                                                     admin_role_permission)
            raise UnauthorizedException('Invalid Permission',
                                        description=description)
        return user_id

    @route('', methods=['GET'])
    @token_auth_required()
    @permissions_required(admin_role_permission)
    @marshal_with(_user_list_schema)
    @paginated
    @extract_args(search_args)
    def list(self, args):
        return auth_datastore.find_users(**args), args


    @token_auth_required()
    @marshal_with_data_envelope(_user_schema)
    def read(self, id):
        id = self._check_current_user_or_admin_role(id)
        user = auth_datastore.read_user(id)
        return user

    @route('', methods=['POST'])
    @one_of(anonymous_required, permissions_required(admin_role_permission))
    @marshal_with_data_envelope(_user_schema)
    @use_args(user_args)
    def create(self, args):
        user = auth_datastore.create_user(**args)
        location = url_for('.users:read', _external=True, **{'id': user.id})
        return user, 201, {
            'Location': location
        }

    @route('<id>', methods=['PUT'])
    @marshal_with_data_envelope(_user_schema)
    @use_args({
        'email': Arg(str, validate=validators.Email()),
        'active': Arg(bool)
    })
    def update(self, args, id):
        id = self._check_current_user_or_admin_role(id)
        return auth_datastore.update_user(id, **args)

    @permissions_required(admin_role_permission)
    def delete(self, id):
        auth_datastore.delete_user(id)
        return ''
