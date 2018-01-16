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
    """
    :param name:
    :param url:
    :return: [
                {
                    'title': 공지사항 제목,
                    'url': 공지사항 URL
                },
                ...
            ]
    """
    original_url = url
    try:
        notice = []

        html_code = requests.get(url)
        html_code.encoding = 'euc-kr' if name != 'IT융합' else None
        soup = BeautifulSoup(html_code.text, "html.parser")

        if name == 'IT융합':
            soup_find = soup.find('table', attrs={'class': 'board-list'}) \
                .findAll('a')
            for s in soup_find:
                s_url = url[:-5] + s.get('href')
                notice.append({
                    'num': int(re.compile('id/([\d]+)').findall(s_url)[0]),
                    'title': s.text,
                    'url': s_url
                })

            return notice

        if name == '홈페이지' or name == '학사공지':
            soup_span_find = soup.find('table', attrs={'class': 'pr_table'}) \
                .findAll('span', attrs={'class': 'gray'})
            soup_find = soup.find('table', attrs={'class': 'pr_table'}) \
                .find('tbody').findAll('a')
            if len(soup_span_find) > 0:
                ss_index = 0
                for ss in soup_span_find:
                    if ss.get('title'):
                        notice.append({
                            'title': ss.get('title')
                        })
                        ss_index += 1

                s_index = 0
                for s in soup_find:
                    if not s.get('title'):
                        s_url = original_url + s.get('href')
                        if s_index <= ss_index:
                            notice[s_index]['num'] = int(re.compile('no=([\d]+)').findall(s_url)[0])
                            notice[s_index]['url'] = s_url

        soup_find = soup.find('table', attrs={'class': 'pr_table'}) \
            .find('tbody').findAll('a')
        for s in soup_find:
            if s.get('title') and not s.get('title') == u'새창열림':
                if name == '컴공' or name == 'SA사업단':
                    s_url = 'http://newclass.hanbat.ac.kr/ctnt/computer/' + s.get('href')
                else:
                    s_url = original_url + s.get('href')
                notice.append({
                    'num': int(re.compile('no=([\d]+)').findall(s_url)[0]),
                    'title': s.get('title'),
                    'url': s_url
                })

        return notice
    except Exception as e:
        log.error(e)
        return [{'title': TEXT_ERROR, 'url': '0'}]


def get_notice(what):
    if what in list(URL_DICT.keys()):
        return crawling(what, URL_DICT[what])
    else:
        return print("파라미터가 없거나 잘못 입력하셨습니다.")


def get_all_notice():
    notice_dict = {}
    notice_max_dict = {}
    for name, url in URL_DICT.items():
        notice_dict[name] = crawling(name, url)
        num_list = [post['num'] for post in notice_dict[name]]
        notice_max_dict[name] = max(num_list) if num_list else 0

    return notice_dict, notice_max_dict
