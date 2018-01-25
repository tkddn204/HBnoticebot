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
    :param name: 크롤링할 이름
    :param url: 크롤링할 URL
    :return: [
                {
                    'title': 공지사항 제목,
                    'url': 공지사항 URL
                },
                ...
            ]
    """
    try:
        notice = []

        html_code = requests.get(url)
        html_code.encoding = 'euc-kr' if name != 'IT융합' else None
        soup = BeautifulSoup(html_code.text, "html.parser")

        if name == 'IT융합':
            soup_find = soup.find('table', attrs={'class': 'board-list'}) \
                .findAll('a')

            max_num = 0
            for s in soup_find:
                s_url = url[:-5] + s.get('href')
                notice.append({
                    'title': s.text,
                    'url': s_url
                })
                num = int(re.compile('id/([\d]+)').findall(s_url)[0])
                max_num = num if max_num <= num else max_num

            return notice, max_num

        soup_find = soup.find('table', attrs={'class': 'pr_table'}) \
            .find('tbody').findAll('a')

        if name == '홈페이지' or name == '학사공지':
            title_list = list(filter(lambda item: item != u'새창열림',
                                re.compile('title="(.+?)"').findall(str(soup_find))))
            url_list = list(filter(lambda item: item.startswith('b'),
                              re.compile('href="(.+?)"').findall(str(soup_find))))
            max_num = max([int(re.compile('no=([\d]+)').findall(url)[0]) for url in url_list])
            for title, path in zip(title_list, url_list):
                notice.append({
                    'title': title,
                    'url': 'http://www.hanbat.ac.kr/_prog/gboard/' + path.replace('&amp;', '&')
                })

            return notice, max_num

        if name == '컴공' or name == 'SA사업단':
            max_num = 0
            for s in soup_find:
                if s.get('title'):
                    s_url = 'http://newclass.hanbat.ac.kr/ctnt/computer/' + s.get('href')
                    notice.append({
                        'title': s.get('title'),
                        'url': s_url
                    })
                    num = int(re.compile('no=([\d]+)').findall(s_url)[0])
                    max_num = num if max_num <= num else max_num

            return notice, max_num

    except Exception as e:
        log.error(e)
        return [{'title': TEXT_ERROR, 'url': '0'}], 0


def get_notice(what):
    if what in URL_DICT.keys():
        return crawling(what, URL_DICT[what])
    else:
        return "파라미터가 없거나 잘못 입력하셨습니다.", 0


def get_all_notice():
    notice_dict = {}
    notice_max_dict = {}
    for name in URL_DICT.keys():
        notice_dict[name], max_num = get_notice(name)
        notice_max_dict[name] = max_num

    return notice_dict, notice_max_dict
