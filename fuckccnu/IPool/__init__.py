# coding: utf-8
"""
    IPool: ip池
    ```````````

    抓取代理, 失效验证, 刷新代理
"""


class IPool(object):
    """IP pool"""

    def __init__(self):
        self.pool = []  # 队列结构模拟ip池

    def getProxy(self, url):
        """从某个网站抓取ip地址"""
        pass

    def refrech(self, ):
        """刷新ip地址"""
        pass
