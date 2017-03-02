#-*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

from text import FIND_THINGS


def crawling(url, *args):
    notice_data = []
    url_data = []
    if args:
        origin_url = url
        for k in args:
            url = url+k
        html_code = requests.get(url)
        html_code.encoding = 'euc-kr'
        soup = BeautifulSoup(html_code.text, "html.parser")
        soup_find = soup.find('table', attrs={'class': 'pr_table'}).find('tbody').findAll('a')
        homepage = '&GotoPage=1' in args
        if homepage:
            soup_span_find = soup.find('table', attrs={'class': 'pr_table'})\
                .findAll('span', attrs={'class': 'gray'})
            for s in soup_span_find:
                if s.get('title'):
                    notice_data.append(s.get('title'))

        for s in soup_find:
            if s.get('title'):
                if not s.get('title') == u'새창열림':
                    notice_data.append(s.get('title'))
                    if not homepage:
                        url_data.append(origin_url + s.get('href'))

            if homepage and not s.get('href').startswith('.'):
                url_data.append(origin_url + s.get('href'))

    else:
        html_code = requests.get(url)
        soup = BeautifulSoup(html_code.text, "html.parser")
        soup_find = soup.find('table', attrs={'class': 'board-list'}).findAll('a')
        url = url.replace('/0201', '')
        for s in soup_find:
            notice_data.append(s.get_text())
            url_data.append(url + s.get('href'))

    # print(notice_data.__len__(), url_data.__len__())
    return notice_data, url_data


def get_notice(what):
    if what == '홈페이지':
        url = 'http://www.hanbat.ac.kr/_prog/gboard/'
        php = 'board.php?code=news'
        notice_list = '&GotoPage=1'
    elif what == '학사공지':
        url = 'http://www.hanbat.ac.kr/_prog/gboard/'
        php = 'board.php?code=bachelor'
        notice_list = '&GotoPage=1'
    elif what == '컴공':
        url = 'http://newclass.hanbat.ac.kr/ctnt/computer/'
        php = 'board.php?mode=list'
        notice_list = '&tbl_cd=computer_notice'
    elif what == 'SA사업단':
        url = 'http://newclass.hanbat.ac.kr/ctnt/computer/'
        php = 'board.php?mode=list'
        notice_list = '&tbl_cd=biz_notice'
    elif what == 'IT융합':
        url = 'http://www.ithanbat.kr/0201'
        return crawling(url)
    else:
        return print("파라메터가 없거나 잘못 입력하셨습니다.")
    return crawling(url, php, notice_list)


def get_max_of_nums(urls, find_things):
    pattern = 'id/([\d]+)' if find_things == 'IT융합' else 'no=([\d]+)'
    r = re.compile(pattern)
    result = '0'
    for u in urls:
        if r.findall(u):
            s = r.findall(u)[0]
            if (s != result) and (int(s) > int(result)):
                result = int(s) if r.search(u) else 0

    return result


def get_max_of_find_things():
    num = []
    for things in FIND_THINGS:
        (find, url) = get_notice(things)
        num.append(get_max_of_nums(url, things))
    return num


def get_nums(urls, find_things):
    pattern = 'id/([\d]+)' if find_things == 'IT융합' else 'no=([\d]+)'
    r = re.compile(pattern)
    result = []
    for u in urls:
        if r.findall(u):
            result.append(int(r.findall(u)[0]))

    return result


def get_all_notice():
    result = {}
    for find_things in FIND_THINGS:
        result[find_things] = {'name': [], 'url': [], 'num': [], 'max': 0}
        result[find_things]['name'], result[find_things]['url'] = get_notice(find_things)
        result[find_things]['num'] = get_nums(result[find_things]['url'], find_things)
        result[find_things]['max'] = get_max_of_nums(result[find_things]['url'], find_things)
    return result


# def test():
#     ''' get notice:
#         홈페이지 : 한밭대 홈페이지 공지사항 목록
#         학사공지 : 한밭대 홈페이지 학사공지 목록
#         컴공 : 컴공 공지사항 목록
#         SA사업단 : SA사업단 공지사항 목록
#         IT융합 : it융합인력양성사업단 목록
#     '''
#     find_things = '컴공'
#     (string, url) = get_notice(find_things)
#     if find_things is 'computer_notice' or find_things is 'sa_notice':
#         print("컴공 서버가 느리므로 자료가 늦게 뜹니다")
#     for u in url:
#         print(u)
#         print(get_nums(u, find_things))
#
# if __name__ == '__main__':
#     test()
