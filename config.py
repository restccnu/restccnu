# coding: utf-8
"""
    config.py
    `````````

    华师匣子API配置

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import os
from datetime import timedelta


class Config(object):
    """
    配置基类
    """
    # 邮件务器配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('RESTCCNU_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('RESTCCNU_MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'muxistudio@163.com'
    MAIL_SUBJECT_PREFIX = 'dead [feedback] bug'
    ADMIN_EMAIL = 'muxistudio@qq.com'

    # 七牛服务配置
    QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY')  # 七牛access key
    QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY')  # 七牛secret key
    QINIU_BUCKET_NAME = os.getenv('QINIU_BUCKET_NAME') or 'ccnustatic'  # 七牛bucket名称
    QINIU_BUCKET_DOMAIN = os.getenv('QINIU_BUCKET_DOMAIN') or 'static.muxixyz.com'  # 七牛资源域名

    # celery消息代理[存储]配置
    CELERY_BROKER_URL = 'redis://@{host}:7383/0'.format(host=os.getenv('REDIS3_HOST'))  # celery消息代理, redis3容器
    CELERY_RESULT_BACKEND = 'redis://@{host}:7383/0'.format(host=os.getenv('REDIS3_HOST')) # celery消息存储, redis3容器
    CELERYBEAT_SCHEDULE = {  # celery beat 定时任务
            'restart_redis_every_86400s': {
                # 每隔1天爬取通知公告
                'task': 'cute_board_spider',
                'schedule': timedelta(seconds=12*3600)
            },
    }

    """
    学年、学期配置
    XNM: 2015 表示 2015~2016学年, 类推
    XQM:
        - 3:  第一学期
        - 12: 第二学期
        - 16: 第三学期
    """
    XNM = os.getenv("RESTCCNU_XNM")
    XQM = os.getenv("RESTCCNU_XQM")


config = {
    # :配置字典: 目前没有做开发、测试、生产环境区分
    # 华师匣子的配置分为2部分:
    #     应用配置 和 环境配置
    # 应用配置服务python project
    # 环境配置基于docker进行开发、测试、部署环境区分
    'develop': Config,
    'test': Config,

    'default': Config
}
