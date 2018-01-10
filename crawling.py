#-*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

from text import TEXT_ERROR
from util.logger import log


URL_DICT = {
    '홈페이지': 'http://www.hanbat.ac.kr/_prog/gboard/board.php?code=news&GotoPage=1',
    '학사공지': 'http://www.hanbat.ac.kr/_prog/gboard/board.php?code=bachelor&GotoPage=1',
    '컴공': 'http://newclass.hanbat.ac.kr/ctnt/computer/board.php?mode=list&tbl_cd=computer_notice',
    'SA사업단': 'http://newclass.hanbat.ac.kr/ctnt/computer/board.php?mode=list&tbl_cd=biz_notice',
    'IT융합': 'http://www.ithanbat.kr/0201',
}


def crawling(name, url):
    original_url = url
    try:
        notice_data, url_data = [], []

        html_code = requests.get(url)
        html_code.encoding = 'euc-kr' if name != 'IT융합' else None
        soup = BeautifulSoup(html_code.text, "html.parser")

        if name == 'IT융합':
            soup_find = soup.find('table', attrs={'class': 'board-list'}) \
                .findAll('a')
            for s in soup_find:
                notice_data.append(s.text)
                url_data.append(url[:-5] + s.get('href'))

            return notice_data, url_data

        if name == '홈페이지' or name == '학사공지':
            soup_span_find = soup.find('table', attrs={'class': 'pr_table'}) \
                .findAll('span', attrs={'class': 'gray'})
            soup_find = soup.find('table', attrs={'class': 'pr_table'}) \
                .find('tbody').findAll('a')
            for ss in soup_span_find:
                if ss.get('title'):
                    notice_data.append(ss.get('title'))
            for s in soup_find:
                if not s.get('title'):
                    url_data.append(original_url + s.get('href'))

        soup_find = soup.find('table', attrs={'class': 'pr_table'}) \
            .find('tbody').findAll('a')
        for s in soup_find:
            if s.get('title') and not s.get('title') == u'새창열림':
                notice_data.append(s.get('title'))
                url_data.append(original_url + s.get('href'))

        return notice_data, url_data
    except Exception as e:
        log.error(e)
        return [TEXT_ERROR], ['0']


def get_notice(what):
    if what in list(URL_DICT.keys()):
        return crawling(what, URL_DICT[what])
    else:
        return print("파라메터가 없거나 잘못 입력하셨습니다.")


def get_nums(urls, name):
        pattern = 'id/([\d]+)' if name == 'IT융합' else 'no=([\d]+)'
        re_com = re.compile(pattern)
        return (int(re_com.findall(u)[0]) if re_com.findall(u) else None for u in urls)


def get_all_notice():
    notice_dict = {}
    notice_max_dict = {}
    for name, url in URL_DICT.items():
        notice_dict[name] = {'name': [], 'url': []}
        notice_dict[name]['name'], notice_dict[name]['url'] = crawling(name, url)
        num_list = get_nums(notice_dict[name]['url'], name)
        notice_max_dict[name] = max(num_list) if num_list else 0
    return notice_dict, notice_max_dict
