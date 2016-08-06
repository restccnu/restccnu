# coding: utf-8
from bs4 import BeautifulSoup
from . import grade_index_url
from . import link_index_url
from . import grade_detail_url
from . import headers


def get_grade_detail(s, sid, xnm, xqm, course, jxb_id):
    grade_detail = {}
    detail_url = grade_detail_url % sid
    link_url = link_index_url
    s.get(link_url)  # 新版与旧版信息门户过渡, 获取cookie
    data = {'xh_id': sid, 'xnm': xnm, 'xqm': xqm,
            'jxb_id': jxb_id, 'kcmc': course}
    r = s.post(detail_url, data, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')
    strings = soup.find('table',
        class_="table table-bordered table-striped table-hover"\
               " tab-bor-col-1 tab-td-padding-5"
    ).tbody.stripped_strings
    _strings = list(strings)
    if len(_strings) == 2:
        usual = ""; ending = ""
    else:
        usual = _strings[2] if len(_strings[2]) < 3 else ""
        ending = _strings[5] if len(_strings[5]) < 3 else ""
    grade_detail.update({
        'usual': usual,
        'ending': ending })
    return grade_detail


def get_grade(s, sid, xnm, xqm):
    grade_url = grade_index_url % sid
    link_url = link_index_url
    s.get(link_url)  # 中转过度, 获取cookie
    post_data = {
        'xnm': xnm, 'xqm': xqm,
        '_search': 'false', 'nd': '1466767885488',
        'queryModel.showCount': 15, 'queryModel.currentPage': 1,
        'queryModel.sortName': "", 'queryModel.sortOrder': 'asc',
        'time': 1 }
    r = s.post(grade_url, post_data)
    json_data = r.json()
    gradeList = []
    # return gradeList
    _gradeList = json_data.get('items')
    for item in _gradeList:
        gradeList.append({
            'course': item.get('kcmc'),
            'credit': item.get('xf'),
            'grade': item.get('cj'),
            'category': item.get('kclbmc'),
            'type': item.get('kcgsmc'),
            'jxb_id': item.get('jxb_id')})
    return gradeList
