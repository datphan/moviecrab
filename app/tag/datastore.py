from abc import abstractmethod, ABCMeta
from datetime import datetime

from flask_security.utils import encrypt_password

from ..datastore import SQLAlchemyDatastore
from ..utils import fix_docs


class TagDatastore(object):
    """Abstract TagDatastore class.

    .. versionadded:: 0.1.0
    """

    __metaclass__ = ABCMeta

    # tags

    @abstractmethod
    def find_tag_list(self, q=None, filters=None, sort=None, offset=None, limit=None, **kwargs):
        """Find all existing tag from the datastore
        by optional query and options.

        .. versionadded:: 0.1.0

        :param q: the optional query as a string which is provided by
                      the current tag, default is None.
        :param filters: the filters list of directory item with keys: (key, op, value)
        :param sort: sorting string (sort='+a,-b,c')
        :param offset: offset (integer positive)
        :param limit: limit (integer positive)
        :param kwargs: the additional keyword arguments containing filter dict {key:value,}

        :return the query
        """
        pass

    @abstractmethod
    def create_tag(self, **kwargs):
        """Creates a new tag associated with the current tag then save it to the database.

        .. versionadded:: 0.1.0

        :param kwargs: the optional kwargs
        :return the created tag
        """
        pass

    @abstractmethod
    def read_tag(self, pid, **kwargs):
        """Reads an existing tag associated with the current tag by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an tag.
        :param kwargs: the optional kwargs.

        :return the found tag
        """
        pass

    @abstractmethod
    def update_tag(self, pid, **kwargs):
        """Updates an existing tag associated with the current tag by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an tag.
        :param kwargs: the optional kwargs.

        :return the updated tag
        """
        pass

    @abstractmethod
    def delete_tag(self, pid, **kwargs):
        """Deletes a existing tag associated with the current tag by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an tag.
        :param kwargs: the optional kwargs
        """
        pass

@fix_docs
class SQLAlchemyTagDatastore(SQLAlchemyDatastore, TagDatastore):
    """
    Implementation for TagDatastore with SQLAlchemy
    """
    # User
    def find_tag_list(self, q=None, filters=None, **kwargs):
        accepted_filter_keys = ('email', 'active')
        kwargs.update({
            'q': q,
            'filters': filters,
            'accepted_filter_keys': accepted_filter_keys
        })

        return self.find_by_model_name('tag', **kwargs)

    def create_tag(self, **kwargs):
        accepted_keys = ('email', 'password', 'active', 'confirmed_at')
        kwargs['password'] = encrypt_password(kwargs['password'])
        # TODO(hoatle): implement verification by signals
        kwargs['active'] = True
        kwargs['confirmed_at'] = datetime.utcnow()
        tag = self.create_by_model_name('tag', accepted_keys, **kwargs)
        tag.roles.append(self.find_roles(name='tag').first())
        self.commit()
        return tag

    def read_tag(self, pid, **kwargs):
        return self.read_by_model_name('tag', pid, **kwargs)

    def update_tag(self, pid, **kwargs):
        return self.update_by_model_name('tag', pid, **kwargs)

    def delete_tag(self, pid, **kwargs):
        self.delete_by_model_name('tag', pid, **kwargs)
