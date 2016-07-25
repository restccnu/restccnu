# coding: utf-8

import os


class Config(object):

    QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY')
    QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY')
    QINIU_BUCKET_NAME = os.getenv('QINIU_BUCKET_NAME')
    QINIU_BUCKET_DOMAIN = os.getenv('QINIU_BUCKET_DOMAIN')


config = {
    'develop': Config,
    'test': Config,

    'default': Config
}
