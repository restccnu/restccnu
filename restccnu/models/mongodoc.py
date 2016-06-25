# coding: utf-8
from mongokit import Document


class User(Document):
    """
    存储用户对应的课表json数据(全部)
    mongodb文档结构: db->collection->data
    """
    __collection__ = 'users'
    __database__ = 'userdb'
    structure = {
            'sid': basestring,
            'table': list
    }
    required_fields = ['sid', 'table']

    def __repr__(self):
        return '<Mongo User>'
