from abc import abstractmethod, ABCMeta
from datetime import datetime

from flask_security.utils import encrypt_password

from ..datastore import SQLAlchemyDatastore
from ..utils import fix_docs


class MovieDatastore(object):
    """Abstract MovieDatastore class.

    .. versionadded:: 0.1.0
    """

    __metaclass__ = ABCMeta

    # movies

    @abstractmethod
    def find_movie_list(self, q=None, filters=None, sort=None, offset=None, limit=None, **kwargs):
        """Find all existing movie from the datastore
        by optional query and options.

        .. versionadded:: 0.1.0

        :param q: the optional query as a string which is provided by
                      the current movie, default is None.
        :param filters: the filters list of directory item with keys: (key, op, value)
        :param sort: sorting string (sort='+a,-b,c')
        :param offset: offset (integer positive)
        :param limit: limit (integer positive)
        :param kwargs: the additional keyword arguments containing filter dict {key:value,}

        :return the query
        """
        pass

    @abstractmethod
    def create_movie(self, **kwargs):
        """Creates a new movie associated with the current movie then save it to the database.

        .. versionadded:: 0.1.0

        :param kwargs: the optional kwargs
        :return the created movie
        """
        pass

    @abstractmethod
    def read_movie(self, pid, **kwargs):
        """Reads an existing movie associated with the current movie by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an movie.
        :param kwargs: the optional kwargs.

        :return the found movie
        """
        pass

    @abstractmethod
    def update_movie(self, pid, **kwargs):
        """Updates an existing movie associated with the current movie by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an movie.
        :param kwargs: the optional kwargs.

        :return the updated movie
        """
        pass

    @abstractmethod
    def delete_movie(self, pid, **kwargs):
        """Deletes a existing movie associated with the current movie by its primary id
        from the database.

        .. versionadded:: 0.1.0

        :param pid: primary id of an movie.
        :param kwargs: the optional kwargs
        """
        pass

@fix_docs
class SQLAlchemyMovieDatastore(SQLAlchemyDatastore, MovieDatastore):
    """
    Implementation for MovieDatastore with SQLAlchemy
    """
    # User
    def find_movie_list(self, q=None, filters=None, **kwargs):
        accepted_filter_keys = ('email', 'active', 'type', 'id')

        if kwargs.get('accepted_filter_keys') is not None:
            accepted_filter_keys = accepted_filter_keys + kwargs.get('accepted_filter_keys')

        kwargs.update({
            'q': q,
            'filters': filters,
            'accepted_filter_keys': accepted_filter_keys
        })

        return self.find_by_model_name('movie', **kwargs)

    def create_movie(self, **kwargs):
        accepted_keys = ('email', 'password', 'active', 'confirmed_at')
        kwargs['password'] = encrypt_password(kwargs['password'])
        # TODO(hoatle): implement verification by signals
        kwargs['active'] = True
        kwargs['confirmed_at'] = datetime.utcnow()
        movie = self.create_by_model_name('movie', accepted_keys, **kwargs)
        movie.roles.append(self.find_roles(name='movie').first())
        self.commit()
        return movie

    def read_movie(self, pid, **kwargs):
        return self.read_by_model_name('movie', pid, **kwargs)

    def update_movie(self, pid, **kwargs):
        return self.update_by_model_name('movie', pid, **kwargs)

    def delete_movie(self, pid, **kwargs):
        self.delete_by_model_name('movie', pid, **kwargs)
