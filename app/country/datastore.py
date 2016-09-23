from abc import abstractmethod, ABCMeta
from datetime import datetime

from flask_security.utils import encrypt_password

from ..datastore import SQLAlchemyDatastore
from ..utils import fix_docs


class CountryDatastore(object):
    """Abstract CountryDatastore class.

    .. versionadded:: 0.1.0
    """

    __metaclass__ = ABCMeta

    # countrys

    @abstractmethod
    def find_country_list(self, q=None, filters=None, sort=None, offset=None, limit=None, **kwargs):
        """Find all existing country from the datastore
        by optional query and options.

        .. versionadded:: 0.1.0

        :param q: the optional query as a string which is provided by
                      the current country, default is None.
        :param filters: the filters list of directory item with keys: (key, op, value)
        :param sort: sorting string (sort='+a,-b,c')
        :param offset: offset (integer positive)
        :param limit: limit (integer positive)
        :param kwargs: the additional keyword arguments containing filter dict {key:value,}

        :return the query
        """
        pass

    @abstractmethod
    def create_country(self, **kwargs):
        """Creates a new country associated with the current country then save it to the database.

        .. versionadded:: 0.1.0

        :param kwargs: the optional kwargs
        :return the created country
        """
        pass

    @abstractmethod
    def read_country(self, pid, **kwargs):
        """Reads an existing country associated with the current country by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an country.
        :param kwargs: the optional kwargs.

        :return the found country
        """
        pass

    @abstractmethod
    def update_country(self, pid, **kwargs):
        """Updates an existing country associated with the current country by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an country.
        :param kwargs: the optional kwargs.

        :return the updated country
        """
        pass

    @abstractmethod
    def delete_country(self, pid, **kwargs):
        """Deletes a existing country associated with the current country by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an country.
        :param kwargs: the optional kwargs
        """
        pass

@fix_docs
class SQLAlchemyCountryDatastore(SQLAlchemyDatastore, CountryDatastore):
    """
    Implementation for CountryDatastore with SQLAlchemy
    """
    # User
    def find_country_list(self, q=None, filters=None, **kwargs):
        accepted_filter_keys = ('email', 'active')
        kwargs.update({
            'q': q,
            'filters': filters,
            'accepted_filter_keys': accepted_filter_keys
        })

        return self.find_by_model_name('country', **kwargs)

    def create_country(self, **kwargs):
        accepted_keys = ('email', 'password', 'active', 'confirmed_at')
        kwargs['password'] = encrypt_password(kwargs['password'])
        # TODO(hoatle): implement verification by signals
        kwargs['active'] = True
        kwargs['confirmed_at'] = datetime.utcnow()
        country = self.create_by_model_name('country', accepted_keys, **kwargs)
        country.roles.append(self.find_roles(name='country').first())
        self.commit()
        return country

    def read_country(self, pid, **kwargs):
        return self.read_by_model_name('country', pid, **kwargs)

    def update_country(self, pid, **kwargs):
        return self.update_by_model_name('country', pid, **kwargs)

    def delete_country(self, pid, **kwargs):
        self.delete_by_model_name('country', pid, **kwargs)

    def filter_by(self, **kwargs):
        return self.filter_by_model_name('country', **kwargs)
    

