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

    用户自定义课表存储
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


class Table(Document):
    """
    :class: table

    信息门户课表存储
    """
    __collection__ = 'tables'
    __database__ = 'tabledb'
    structure = {
        'sid': basestring,
        'table': list
    }
    required_fields = ['sid', 'table']

    def __repr__(self):
        return '<Mongo Table>'


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


class Attention(Document):
    """
    :class: Attention

    用户图书关注存储
    """
    __collection__ = 'attentions'
    __database__ = 'attendb'
    structure = {
        'book_name': basestring,
        'sid': list
    }
    required_fields = ['bar_code', 'book_info', 'sid']

    def __repr__(self):
        return '<Mongo Attention>'


class Classroom(Document):
    """
    :class: Classroom

    空闲教室存储
    """
    __collection__ = 'classrooms'
    __database__ = 'roomdb'
    structure = {
            'weekNo': basestring,
            'mon': dict,
            'tue': dict,
            'wed': dict,
            'thu': dict,
            'fri': dict
    }
    required_fields = ['mon', 'tue', 'wed', 'thu', 'fri']

    def __repr__(self):
        return '<Mongo Classroom>'
