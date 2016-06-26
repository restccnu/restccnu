# coding: utf-8
import requests
# from . import ele_index_url
# from . import headers
ele_index_url = "http://202.114.38.46/"
headers = {
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Accept-Encoding':"gzip, deflate",
}


def get_ele():
    data = {
        'ScriptManager1': 'UpdatePane12|ddlFloor',
        'ddlArea': '1', 'ddlArc': '1', 'ddlFloor': '1',
        '_EVENTTARGET': 'ddlFloor'
    }
    # 现在基本的思路就是建立索引表 index
    r = requests.post(ele_index_url, data)
    return r.content


if __name__ == '__main__':
    print get_ele()
