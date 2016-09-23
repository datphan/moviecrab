"""pagination for sqlalchemy"""

from flask import current_app, request, url_for

from .utils import merge_dict

import math

class Pagination(object):
    def __init__(self, query, before=None, after=None, limit=None, **kwargs):
        self.limit_range = kwargs.get('limit_range') or 3

    @property
    def total_page(self):
        return int(
                    math.ceil(
                        float(self.count) / self.limit
                    )
                )

    @property
    def current_page(self):
        return int(
                    math.ceil(
                        math.floor(
                            (self.limit + self.offset) / self.limit
                        )
                    )
                )

    @property
    def first_range(self):
        value = self.current_page - self.limit_range

        return 0 if value <= 0 else value

    @property
    def last_range(self):
        value = self.current_page + self.limit_range

        return self.total_page if value >= self.total_page else value

    def get_page_url(self, page_number):
        return self.page_url(page_number * self.limit, self.limit)


# TODO(hoatle): implement this
class CursorPagination(object):
    """cursor-based pagination,
    see: https://developers.facebook.com/docs/graph-api/using-graph-api/v2.4"""
    def __init__(self, query, before=None, after=None, limit=None):
        pass


# TODO(hoatle): implement this
class TimePagination(object):
    """time-based pagination,
    see: https://developers.facebook.com/docs/graph-api/using-graph-api/v2.4"""
    def __init__(self, query, since=None, until=None, limit=None):
        pass


class OffsetPagination(Pagination):
    """offset-based pagination,
    see: https://developers.facebook.com/docs/graph-api/using-graph-api/v2.4"""

    def __init__(self, query, offset=None, limit=None, **kwargs):
        """initialize the offset based pagination
        :param query the query instance
        :param offset optional offset
        :param limit official limit
        """
        super(OffsetPagination, self).__init__(query, offset, limit, **kwargs)

        pagination_limit = current_app.config.get('PAGINATION_LIMIT', 25)

        if offset is None:
            self.offset = 0
        elif offset < 0:
            raise ValueError('offset is negative({}), should be positive or zero'.format(offset))
        else:
            self.offset = offset

        if limit is None:
            self.limit = pagination_limit
        elif limit <= 0:
            raise ValueError('limit is negative({}), should be positive'.format(limit))
        else:
            self.limit = limit if limit <= pagination_limit else pagination_limit

        self.count = query.offset(None).limit(None).count()
        self.data = query.offset(self.offset).limit(self.limit).all()

    @property
    def has_prev(self):
        """Check if the pagination has a previous page"""
        return (self.offset - self.limit) > -1  # as offset is 0 based

    @property
    def has_next(self):
        """Check if the pagination has a next page"""
        return (self.offset + self.limit) < self.count

    @property
    def prev_url(self):
        """Get the previous page url if any"""
        if self.has_prev:
            offset = self.offset - self.limit
            return self.page_url(offset, self.limit)
        return None

    @property
    def next_url(self):
        """Get the next page url if any"""
        if self.has_next:
            offset = self.offset + self.limit
            return self.page_url(offset, self.limit)
        return None

    @staticmethod
    def page_url(offset, limit):
        """Construct the page url from the provided offset and limit"""
        args = merge_dict(request.view_args, request.values.to_dict())
        args['offset'] = offset
        args['limit'] = limit
        return url_for(request.endpoint, _external=True, **args)
