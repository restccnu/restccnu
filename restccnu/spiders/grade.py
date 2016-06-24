# coding: utf-8


def get_grade(s, sid, xnm, xqm):
    grade_url = "http://122.204.187.6/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdmKey=N305005&sessionUserKey=%s" % sid
    link_url = "http://portal.ccnu.edu.cn/roamingAction.do?appId=XK"
    s.get(link_url)  # 中转过度, 获取cookie
    post_data = {
        'xnm': xnm,
        'xqm': xqm,
        '_search': 'false',
        'nd': '1466767885488',
        'queryModel.showCount': 15,
        'queryModel.currentPage': 1,
        'queryModel.sortName': "",
        'queryModel.sortOrder': 'asc',
        'time': 1
    }
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
            'category': item.get('kcxzmc')
        })
    return gradeList
