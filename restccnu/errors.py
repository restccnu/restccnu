# coding: utf-8


class ForbiddenError(Exception):
    def __init__(self):
        self.status_code = 403

    def __repr__(self):
        return "{'msg': 'forbidden'}"


class NotfoundError(Exception):
    def __init__(self):
        self.status_code = 404

    def __repr__(self):
        return "{'msg': 'notfound'}"
