#-*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

# SSL 인증서 문제로 인한 경고 메세지 로그 해제
import urllib3
urllib3.disable_warnings()

from text import TEXT_ERROR
from util.logger import log
from urls import URL_DICT

def crawling(name, url):
    """ 공지사항 크롤링 메소드

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

        html_code = requests.get(url, verify=False)
        html_code.encoding = 'euc-kr' if name != 'IT융합' else None
        soup = BeautifulSoup(html_code.text, "html.parser")

        if name == 'IT융합':
            soup_find = soup.find('table', attrs={'class': 'board-list'}) \
                .findAll('a')

            max_num = 0
            for s in soup_find:
                s_url = url[:-5] + s.get('href')
                num = int(re.compile('id/([\d]+)').findall(s_url)[0])
                notice.append({
                    'num': num,
                    'title': s.text,
                    'url': s_url
                })
                max_num = num if max_num <= num else max_num

            return notice, max_num

        soup_find = soup.find('table', attrs={'class': 'pr_table'}) \
            .find('tbody').findAll('a')

        if name == '홈페이지' or name == '학사공지' or name == '학생참여행사':
            title_list = list(filter(lambda item: item != u'새창열림',
                                     re.compile('title="(.+?)"').findall(str(soup_find))))
            url_list = list(filter(lambda item: item.startswith('b'),
                                   re.compile('href="(.+?)"').findall(str(soup_find))))
            num_list = [int(re.compile('no=([\d]+)').findall(url)[0]) for url in url_list]
            max_num = max(num_list)
            for title, path, num in zip(title_list, url_list, num_list):
                notice.append({
                    'num': num,
                    'title': title,
                    'url': 'https://www.hanbat.ac.kr/_prog/gboard/' + path.replace('&amp;', '&')
                })

            return notice, max_num

        if name == '컴공' or name == 'SA사업단':
            max_num = 0
            for s in soup_find:
                if s.get('title'):
                    s_url = 'http://newclass.hanbat.ac.kr/ctnt/computer/' + s.get('href')
                    num = int(re.compile('no=([\d]+)').findall(s_url)[0])
                    notice.append({
                        'num': num,
                        'title': s.get('title'),
                        'url': s_url
                    })
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
