# coding: utf-8
from .mongodoc import User
from mongokit import Connection


# config
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27020

#  使用mongodb进行课表数据存储
connection = Connection(MONGODB_HOST, MONGODB_PORT)
connection.register([User])
