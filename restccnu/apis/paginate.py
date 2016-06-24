# coding: utf-8

from json import JSONEncoder
from collections import MutableSequence
from flask import url_for


class _Pagination(MutableSequence, JSONEncoder):
    """
    pagination class
    """
    def __init__(self, resources, current, per_page):
        super(_Pagination, self).__init__()
        self._resources = resources
        self._num = per_page
        self._sum = len(resources)
        self._pages = self._sum // self._num
        if self._sum % self._num != 0:
            self._pages += 1
        self._current = current
        self.next_page = url_for('api.api_search_books',
                                 page=self._current+1, _external=True) \
            if self.has_next() else ""
        self.last_page = url_for('api.api_search_books',
                                 page=self._pages, _external=True)

    def __len__(self):
        return self._sum

    def __getitem__(self, i):
        return self._resources[i]

    def __setitem__(self, i, var):
        self._resources[i] = var

    def __delitem__(self, i):
        del self._resources[i]

    def insert(self, i, var):
        self._resources.insert(i, var)

    def append(self, var):
        self.insert(self._sum, var)

    def has_next(self):
        return True if self._current < self._pages else False

    def __repr__(self):
        return "Pagination on %r" % self._resources
