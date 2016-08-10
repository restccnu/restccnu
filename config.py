# coding: utf-8

import os


class Config(object):

    QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY')
    QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY')
    QINIU_BUCKET_NAME = os.getenv('QINIU_BUCKET_NAME') or 'ccnustatic'
    QINIU_BUCKET_DOMAIN = os.getenv('QINIU_BUCKET_DOMAIN') or 'oao7x1n3m.bkt.clouddn.com'

    XNM = 2015
    XQM = 12


config = {
    'develop': Config,
    'test': Config,

    'default': Config
}
