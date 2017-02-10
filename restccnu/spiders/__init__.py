# coding: utf-8
"""
    spiders
    ```````

    华师爬虫misaka~华师匣子后端核心!
        - requests + bs4
    Hi, misaka spider:)

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""
import os
import random
from fuckccnu.multiUA import LoadUserAgents

"""
headers
-> 随机UserAgent
"""
uas = LoadUserAgents()
ua = random.choice(uas)
headers = { 'User-Agent': ua }

"""
proxy
-> 校内SOCKS5代理, 防止万恶的学校封外网
"""
PROXY = os.getenv("PROXY")
if PROXY == "ON":
    proxy = {
            'http': 'socks5:127.0.0.1:1080',
            'https': 'socks5:127.0.0.1:1080'
    }
elif PROXY == "OFF": proxy = None

# URL MAP
"""模拟登录"""
info_login_url = "http://portal.ccnu.edu.cn/loginAction.do"
info_login_test_url = "http://portal.ccnu.edu.cn/chpass.jsp"
lib_login_url = "http://202.114.34.15/reader/redr_verify.php"
lib_login_test_url = "http://202.114.34.15/reader/redr_info.php"
link_index_url = "http://portal.ccnu.edu.cn/roamingAction.do?appId=XK"

"""图书馆"""
lib_search_url = "http://202.114.34.15/opac/openlink.php"
lib_me_url = "http://202.114.34.15/reader/book_lst.php"
lib_detail_url = "http://202.114.34.15/opac/item.php?marc_no=%s"
lib_renew_url = "http://202.114.34.15/reader/ajax_renew.php"
douban_url = "https://api.douban.com/v2/book/isbn/%s"

"""课程表"""
table_test_url = "http://portal.ccnu.edu.cn/index_jg.jsp"
table_index_url = "http://122.204.187.6/kbcx/xskbcx_cxXsKb.html?gnmkdmKey=N253508&sessionUserKey=%s"

"""成绩查询"""
grade_index_url = "http://122.204.187.6/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdmKey=N305005&sessionUserKey=%s"
grade_detail_url = "http://122.204.187.6/cjcx/cjcx_cxCjxq.html?time=1468243324589&gnmkdmKey=N305005&sessionUserKey=%s"

"""电费查询"""
ele_index_url = "http://202.114.38.46/"
ele_url = "http://202.114.38.46/SelectPage.aspx/SerBindTabDate"
new_ele_url = "http://jnb.ccnu.edu.cn/weixin/example/demo/search.php"

"""通知公告"""
zizhu_url = 'http://zizhu.ccnu.edu.cn/index.htm'
huaqing_url = 'http://www.ccnuyouth.com/tzgg.htm'
jiaowuchu1 = 'http://jwc.ccnu.edu.cn/index/tzggxs.htm'
jiaowuchu2 = 'http://jwc.ccnu.edu.cn/index/tzggxy.htm'
myccnu_url = 'http://ccnu.chunkao.cn'
myccnu_cookie = 'PHPSESSID=uv2cdkv1uql14ofgmoe5ob4e44'
