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
import random
from fuckccnu.multiUA import LoadUserAgents

"""
headers
-> 随机UserAgent
"""
uas = LoadUserAgents()
ua = random.choice(uas)
headers = {
        'User-Agent': ua,
        'Connection': 'close',
}


"""
proxy
-> 校内服务代理, 防止万恶的学校封外网
"""
proxy = {
    "https": "https://:fuckccnu@218.199.196.131:8388"
}


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
douban_url = "https://api.douban.com/v2/book/isbn/%s"

"""课程表"""
table_test_url = "http://portal.ccnu.edu.cn/index_jg.jsp"
table_index_url = "http://122.204.187.6/kbcx/xskbcx_cxXsKb.html?gnmkdmKey=N253508&sessionUserKey=%s"

"""成绩查询"""
grade_index_url = "http://122.204.187.6/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdmKey=N305005&sessionUserKey=%s"
grade_detail_url = "http://122.204.187.6/cjcx/cjcx_cxCjxq.html?time=1468243324589&gnmkdmKey=N305005&sessionUserKey=%s"

"""电费查询"""
ele_index_url = "http://202.114.38.46/"

"""通知公告"""
zizhu_url = 'http://zizhu.ccnu.edu.cn/index.htm'
huaqing_url = 'http://www.ccnuyouth.com/tzgg.htm'
jiaowuchu1 = 'http://jwc.ccnu.edu.cn/index/tzggxs.htm'
jiaowuchu2 = 'http://jwc.ccnu.edu.cn/index/tzggxy.htm'
myccnu_url = 'http://ccnu.chunkao.cn'
myccnu_cookie = 'PHPSESSID=uv2cdkv1uql14ofgmoe5ob4e44'
