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
    required_fields = ['sid']

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
    required_fields = ['sid']

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
        'bid': basestring,
        'book': basestring,
        'id': basestring,
        'author': basestring,
        'sid': basestring
    }

    def __repr__(self):
        return '<Mongo Attention>'


class Week(Document):
    """
    :class: Week

    每周空闲教室存储
    """
    __collection__ = 'weeks'
    __database__ = 'weekdb'
    structure = {
            'bno': unicode,
            'weekNo': unicode,
            'mon': dict,
            'tue': dict,
            'wed': dict,
            'thu': dict,
            'fri': dict
    }

    def __repr__(self):
        return '<Mongo Week bno:{} weekNo:{}>'.format(self['bno'], self['weekNo'])


class Feedback(Document):
    """
    :class: Feedback

    ios用户反馈存储
    """
    __collection__ = 'feedbacks'
    __database__ = 'feedb'
    structure = {
        'contact': basestring,
        'feedback': basestring
    }
    required_fields = ['feedback', 'contact']

    def __repr__(self):
        return '<Mongo Feedback>'
