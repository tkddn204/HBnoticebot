from crawling import get_notice, get_all_notice
from pprint import pprint

def test_get_all_notice():
    notice, notice_max = get_all_notice()
    pprint(notice)
    print("----------------------------")
    pprint(notice_max)


def test_get_notice(what: str):
    pprint(get_notice(what))


test_get_all_notice()
# test_get_notice("홈페이지")
# test_get_notice("학사공지")
# test_get_notice("IT융합")
# test_get_notice("컴공")
# test_get_notice("SA사업단")
# test_get_notice("asdf")

# def test():
#     ''' get notice:
#         홈페이지 : 한밭대 홈페이지 공지사항 목록
#         학사공지 : 한밭대 홈페이지 학사공지 목록
#         컴공 : 컴공 공지사항 목록
#         SA사업단 : SA사업단 공지사항 목록
#         IT융합 : it융합인력양성사업단 목록
#     '''
#     find_things = '홈페이지'
#     (string, url) = get_notice(find_things)
#     if find_things is 'computer_notice' or find_things is 'sa_notice':
#         print("컴공 서버가 느리므로 자료가 늦게 뜹니다")
#     for u in url:
#         print(u)
#         print(get_nums(u, find_things))
#
# if __name__ == '__main__':
#     test()
