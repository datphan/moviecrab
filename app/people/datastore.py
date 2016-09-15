from abc import abstractmethod, ABCMeta
from datetime import datetime

from flask_security.utils import encrypt_password

from ..datastore import SQLAlchemyDatastore
from ..utils import fix_docs


class PeopleDatastore(object):
    """Abstract PeopleDatastore class.

    .. versionadded:: 0.1.0
    """

    __metaclass__ = ABCMeta

    # peoples

    @abstractmethod
    def find_people_list(self, q=None, filters=None, sort=None, offset=None, limit=None, **kwargs):
        """Find all existing people from the datastore
        by optional query and options.

        .. versionadded:: 0.1.0

        :param q: the optional query as a string which is provided by
                      the current people, default is None.
        :param filters: the filters list of directory item with keys: (key, op, value)
        :param sort: sorting string (sort='+a,-b,c')
        :param offset: offset (integer positive)
        :param limit: limit (integer positive)
        :param kwargs: the additional keyword arguments containing filter dict {key:value,}

        :return the query
        """
        pass

    @abstractmethod
    def create_people(self, **kwargs):
        """Creates a new people associated with the current people then save it to the database.

        .. versionadded:: 0.1.0

        :param kwargs: the optional kwargs
        :return the created people
        """
        pass

    @abstractmethod
    def read_people(self, pid, **kwargs):
        """Reads an existing people associated with the current people by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an people.
        :param kwargs: the optional kwargs.

        :return the found people
        """
        pass

    @abstractmethod
    def update_people(self, pid, **kwargs):
        """Updates an existing people associated with the current people by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an people.
        :param kwargs: the optional kwargs.

        :return the updated people
        """
        pass

    @abstractmethod
    def delete_people(self, pid, **kwargs):
        """Deletes a existing people associated with the current people by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an people.
        :param kwargs: the optional kwargs
        """
        pass

@fix_docs
class SQLAlchemyPeopleDatastore(SQLAlchemyDatastore, PeopleDatastore):
    """
    Implementation for PeopleDatastore with SQLAlchemy
    """
    # User
    def find_people_list(self, q=None, filters=None, **kwargs):
        accepted_filter_keys = ('email', 'active')
        kwargs.update({
            'q': q,
            'filters': filters,
            'accepted_filter_keys': accepted_filter_keys
        })

        return self.find_by_model_name('people', **kwargs)

    def create_people(self, **kwargs):
        accepted_keys = ('email', 'password', 'active', 'confirmed_at')
        kwargs['password'] = encrypt_password(kwargs['password'])
        # TODO(hoatle): implement verification by signals
        kwargs['active'] = True
        kwargs['confirmed_at'] = datetime.utcnow()
        people = self.create_by_model_name('people', accepted_keys, **kwargs)
        people.roles.append(self.find_roles(name='people').first())
        self.commit()
        return people

    def read_people(self, pid, **kwargs):
        return self.read_by_model_name('people', pid, **kwargs)

    def update_people(self, pid, **kwargs):
        return self.update_by_model_name('people', pid, **kwargs)

    def delete_people(self, pid, **kwargs):
        self.delete_by_model_name('people', pid, **kwargs)
