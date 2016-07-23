# coding: utf-8

import os


class Config(object):

    QINIU_ACCESS_KEY = os.getenv('restccnu_qiniu_ak')
    QINIU_SECRET_KEY = os.getenv('restccnu_qiniu_sk')
    QINIU_BUCKET_NAME = 'ccnustatic'
    QINIU_BUCKET_DOMAIN = 'oao7x1n3m.bkt.clouddn.com'


config = {
    'develop': Config,
    'test': Config,

    'default': Config
}
