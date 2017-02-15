#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


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
        for s in soup_find:
            if s.get('title'):
                if not s.get('title') == u'새창열림':
                    notice_data.append(s.get('title'))
                    url_data.append(origin_url + s.get('href'))
    else:
        html_code = requests.get(url)
        soup = BeautifulSoup(html_code.text, "html.parser")
        soup_find = soup.find('table', attrs={'class': 'board-list'}).findAll('a')
        url = url.replace('/0201', '')
        for s in soup_find:
            notice_data.append(s.get_text())
            url_data.append(url + s.get('href'))
    return notice_data, url_data


def get_notice(what):
    if what == '홈페이지':
        url = 'http://www.hanbat.ac.kr/_prog/gboard/'
        php = 'board.php?code=news'
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


def test():
    ''' get notice:
        홈페이지 : 한밭대 홈페이지 공지사항 목록
        컴공 : 컴공 공지사항 목록
        SA사업단 : SA사업단 공지사항 목록
        IT융합 : it융합인력양성사업단 목록
    '''
    find_things = '홈페이지'
    data = get_notice(find_things)
    if find_things is 'computer_notice' or find_things is 'sa_notice':
        print("컴공 서버가 느리므로 자료가 늦게 뜹니다")
    for d in data:
        print(d)

if __name__ == '__main__':
    test()