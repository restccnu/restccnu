# coding: utf-8
"""
    paginate.py
    ```````````

    资源分页模块

    :MAINTAINER: neo1218
    :OWNER: muxistudio

"""

from json import JSONEncoder
from collections import MutableSequence
from flask import url_for


class _Pagination(MutableSequence, JSONEncoder):
    """
    :class: _Pagination

    资源分页
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
        self.max_page = self._pages

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
