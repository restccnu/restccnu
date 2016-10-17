# coding: utf-8
"""
    mongodoc.py
    ```````````

    mongodb数据库文档结构定义, 使用mongokit

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""
from mongokit import Document


class User(Document):
    """
    :class: User

    用户课表存储
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


class Dormitory(Document):
    """
    :class: Dormitory

    宿舍电表存储
    """
    __collection__ = 'dormitories'
    __database__ = 'dordb'
    structure = {
            'meter': dict
    }
    required_fields = ['meter']

    def __repr__(self):
        return '<Mongo Dormitory>'
