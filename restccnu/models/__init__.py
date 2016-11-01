# coding: utf-8
"""
    models
    ``````

    mongodb数据库存储
        - 课表存储: 存储自定义课表
        - 寝室电表号存储: 存储爬取的寝室电表号

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import os
from .mongodoc import User, Dormitory, Table
from mongokit import Connection


# config
MONGODB_HOST = os.getenv("REST_MONGO_HOST")
MONGODB_PORT = 27020

#  使用mongodb进行课表数据存储
connection = Connection(MONGODB_HOST, MONGODB_PORT)
connection.register([User])
connection.register([Dormitory])
connection.register([Table])

# _zero: 占位课程, id=0
## mongodb😓 的特性, 只有数据写入的时候创建数据库
_zero = {
    "id": "0",
    "course": "re:从零开始的异世界生活",
    "teacher": "neo1218",
    "weeks": "1",
    "day": "2",
    "start": "3",
    "during": "4",
    "place": "5",
    "remind": False
}
