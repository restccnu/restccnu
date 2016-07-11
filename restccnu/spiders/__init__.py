# coding: utf-8
# URL Map :)

"""模拟登录"""
info_login_url = "http://portal.ccnu.edu.cn/loginAction.do"
info_login_test_url = "http://portal.ccnu.edu.cn/chpass.jsp"
lib_login_url = "http://202.114.34.15/reader/redr_verify.php"
lib_login_test_url = "http://202.114.34.15/reader/redr_info.php"
headers = {
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Accept-Encoding':"gzip, deflate",
}


"""图书馆"""
lib_search_url = "http://202.114.34.15/opac/openlink.php"
lib_me_url = "http://202.114.34.15/reader/book_lst.php"
lib_detail_url = "http://202.114.34.15/opac/item.php?marc_no=%s"
douban_url = "https://api.douban.com/v2/book/isbn/%s"


"""课程表"""
table_test_url = "http://portal.ccnu.edu.cn/index_jg.jsp"
table_index_url = "http://122.204.187.6/kbcx/xskbcx_cxXsKb.html?gnmkdmKey=N253508&sessionUserKey=%s"
link_index_url = "http://portal.ccnu.edu.cn/roamingAction.do?appId=XK"


"""成绩查询"""
grade_index_url = "http://122.204.187.6/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdmKey=N305005&sessionUserKey=%s"
grade_detail_url = "http://122.204.187.6/cjcx/cjcx_cxCjxq.html?time=1468243324589&gnmkdmKey=N305005&sessionUserKey=%s"


"""电费查询"""
ele_index_url = "http://202.114.38.46/"


"""通知公告"""
zizhu_url = 'http://zizhu.ccnu.edu.cn/index.php?m=content&c=index&a=lists&catid=268'
huaqing_url = 'http://www.ccnuyouth.com/a/notice/'
jiaowuchu_url = 'http://jwc.ccnu.edu.cn/index/tzggxs.htm'
