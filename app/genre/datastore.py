from abc import abstractmethod, ABCMeta
from datetime import datetime

from flask_security.utils import encrypt_password

from ..datastore import SQLAlchemyDatastore
from ..utils import fix_docs


class GenreDatastore(object):
    """Abstract GenreDatastore class.

    .. versionadded:: 0.1.0
    """

    __metaclass__ = ABCMeta

    # genres

    @abstractmethod
    def find_genre_list(self, q=None, filters=None, sort=None, offset=None, limit=None, **kwargs):
        """Find all existing genre from the datastore
        by optional query and options.

        .. versionadded:: 0.1.0

        :param q: the optional query as a string which is provided by
                      the current genre, default is None.
        :param filters: the filters list of directory item with keys: (key, op, value)
        :param sort: sorting string (sort='+a,-b,c')
        :param offset: offset (integer positive)
        :param limit: limit (integer positive)
        :param kwargs: the additional keyword arguments containing filter dict {key:value,}

        :return the query
        """
        pass

    @abstractmethod
    def create_genre(self, **kwargs):
        """Creates a new genre associated with the current genre then save it to the database.

        .. versionadded:: 0.1.0

        :param kwargs: the optional kwargs
        :return the created genre
        """
        pass

    @abstractmethod
    def read_genre(self, pid, **kwargs):
        """Reads an existing genre associated with the current genre by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an genre.
        :param kwargs: the optional kwargs.

        :return the found genre
        """
        pass

    @abstractmethod
    def update_genre(self, pid, **kwargs):
        """Updates an existing genre associated with the current genre by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an genre.
        :param kwargs: the optional kwargs.

        :return the updated genre
        """
        pass

    @abstractmethod
    def delete_genre(self, pid, **kwargs):
        """Deletes a existing genre associated with the current genre by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an genre.
        :param kwargs: the optional kwargs
        """
        pass

@fix_docs
class SQLAlchemyGenreDatastore(SQLAlchemyDatastore, GenreDatastore):
    """
    Implementation for GenreDatastore with SQLAlchemy
    """
    # User
    def find_genre_list(self, q=None, filters=None, **kwargs):
        accepted_filter_keys = ('email', 'active')
        kwargs.update({
            'q': q,
            'filters': filters,
            'accepted_filter_keys': accepted_filter_keys
        })

        return self.find_by_model_name('genre', **kwargs)

    def create_genre(self, **kwargs):
        accepted_keys = ('email', 'password', 'active', 'confirmed_at')
        kwargs['password'] = encrypt_password(kwargs['password'])
        # TODO(hoatle): implement verification by signals
        kwargs['active'] = True
        kwargs['confirmed_at'] = datetime.utcnow()
        genre = self.create_by_model_name('genre', accepted_keys, **kwargs)
        genre.roles.append(self.find_roles(name='genre').first())
        self.commit()
        return genre

    def read_genre(self, pid, **kwargs):
        return self.read_by_model_name('genre', pid, **kwargs)

    def update_genre(self, pid, **kwargs):
        return self.update_by_model_name('genre', pid, **kwargs)

    def delete_genre(self, pid, **kwargs):
        self.delete_by_model_name('genre', pid, **kwargs)

    def filter_by(self, **kwargs):
        return self.filter_by_model_name('genre', **kwargs)


