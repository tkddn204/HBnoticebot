from crawling import get_all_notice


def test():
    notice, notice_max = get_all_notice()
    for name, list in notice.items():
        print(name)
        for key, val in list.items():
            print(key, ":", val)

    for k, v in notice_max.items():
        print(k, v)

test()

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
