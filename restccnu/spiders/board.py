# -*- coding: utf-8 -*-
import urllib
import sys
from bs4 import BeautifulSoup

from . import zizhu_url
from . import huaqing_url
from . import jiaowuchu_url


reload(sys)
sys.setdefaultencoding('utf-8')



def get_zizhu_html():
    zizhu_page = urllib.urlopen(zizhu_url)
    zizhu_html = zizhu_page.read()
    zizhu_soup = BeautifulSoup(zizhu_html, "lxml")
    zizhu_list = zizhu_soup.find_all('ul')[2].find_all('li')[:5]
    result_list = []
    for i in zizhu_list:
        title = i.a.contents[0]
        date = i.span.contents[0]
        content_url = i.a['href']
        content_page = urllib.urlopen(content_url)
        content_html = content_page.read()
        content_soup = BeautifulSoup(content_html, "lxml")
        content_strings = content_soup.find_all('div', id='details')[0].strings
        content_appendix_url_list = []
        content_appendix_list = content_soup.find_all('div', id='details')[0].find_all('a')
        if content_appendix_list:
            for m in content_appendix_list:
                content_appendix_url_list.append(m['href'])
        content_string = " "
        for n in content_strings:
            content_string += n
        if ('<' in content_string) and ('>' in content_string):
            sindex = content_string.index('<')
            eindex = content_string.index('>')
            content_string_result = content_string[:sindex] + content_string[eindex+1:]
        else:
            content_string_result = content_string
        result_list.append({
            'title': title,
            'content': content_string_result.strip(),
            'date': date,
            'appendix_list': content_appendix_url_list
            })
    return result_list


def get_huaqing_html():
    huaqing_page = urllib.urlopen(huaqing_url)
    huaqing_html = huaqing_page.read()
    huaqing_soup = BeautifulSoup(huaqing_html, "lxml")
    huaqing_list = huaqing_soup.find_all('ul', class_='e2')[0].find_all('li')[:5]
    result_list = []
    for i in huaqing_list:
        title = i.a.contents[0]
        date = i.contents[-1]
        content_url = "http://www.ccnuyouth.com" + i.a['href']
        content_page = urllib.urlopen(content_url)
        content_html = content_page.read()
        content_soup = BeautifulSoup(content_html, "lxml")
        content_strings = content_soup.find_all('div', class_='newsBody')[0].strings
        content_appendix_url_list = []
        content_appendix_list = content_soup.find_all('div', class_='newsBody')[0].find_all('a')
        if content_appendix_list:
            for m in content_appendix_list:
                if m.has_attr('href'):
                    ahref = m['href']
                    if ahref[:4] == 'http':
                        content_appendix_url_list.append(ahref)
        content_string = " "
        for n in content_strings:
            content_string += n
        if ('function' in content_string) and ('Commets(1);' in content_string):
            sindex = content_string.index('function')
            eindex = content_string.index('Commets(1);')
            content_string_result1 = content_string[:sindex] + content_string[eindex+11:]
        else:
            content_string_result1 = content_string
        if ('请自觉遵守互联网相关的政策法规' in content_string_result1) and ('发表评论' in content_string_result1):
            sindex = content_string.index('请自觉遵守互联网相关的政策法规')
            eindex = content_string.index('发表评论')
            content_string_result2 = content_string_result1[:sindex] + content_string_result1[eindex+4:]
        else:
            content_string_result2 = content_string_result1
        result_list.append({
            'title': title,
            'content': content_string_result2.strip(),
            'date': date,
            'appendix_list': content_appendix_url_list
            })
    return result_list


def get_jiaowuchu_html():
    jiaowuchu_page = urllib.urlopen(jiaowuchu_url)
    jiaowuchu_html = jiaowuchu_page.read()
    jiaowuchu_soup = BeautifulSoup(jiaowuchu_html, "lxml")
    jiaowuchu_list = jiaowuchu_soup.find_all('ul')[11].find_all('li')[:5]
    result_list = []
    for i in jiaowuchu_list:
        title = i.a.contents[0]
        date = i.span.next_sibling.next_sibling.contents[0]
        content_url = 'http://jwc.ccnu.edu.cn' + i.a['href'][2:]
        content_page = urllib.urlopen(content_url)
        content_html = content_page.read()
        content_soup = BeautifulSoup(content_html, "lxml")
        content_strings = content_soup.find_all('div', class_='xwcon')[0].strings
        content_appendix_url_list = []
        if content_soup.find_all('ul', style='list-style-type:none'):
            content_appendix_list = content_soup.find_all('ul', style='list-style-type:none')[0].find_all('li')
            if content_appendix_list:
                for i in content_appendix_list:
                    content_appendix_url_list.append(i.a['href'])
        content_string = " "
        for n in content_strings:
            content_string += n
        if ('<' in content_string) and ('>' in content_string):
            sindex = content_string.index('<')
            eindex = content_string.index('>')
            content_string_result = content_string[:sindex] + content_string[eindex+1:]
        else:
            content_string_result = content_string
        result_list.append({
            'title': title,
            'content': content_string_result.strip(),
            'date': date,
            'appendix_list': content_appendix_url_list
            })
    return result_list


def get_all_board():
    zizhu_list = get_zizhu_html()
    huaqing_list = get_huaqing_html()
    jiaowuchu_list = get_jiaowuchu_html()
    board_list = zizhu_list + huaqing_list +jiaowuchu_list
    return board_list
