# using sqlite3(peewee)
# -*- coding: utf-8 -*-
from db.models import Notices
from db import *


class BotDB:
    def __init__(self):
        db.connect()
        db.create_table(Notices, safe=True)

    # Notices
    def get_notice(self, notice_id=None, name=None):
        try:
            if notice_id:
                return Notices.get(Notices.id == notice_id)
            elif name:
                return Notices.get(Notices.name == name)
            else:
                # return list
                return Notices.select()
        except Notices.DoesNotExist:
            return None

    def get_notice_nums(self):
        return Notices.select(Notices.num)

    def create_notice(self, name):
        notice = ''
        if isinstance(name, list):
            for n in name:
                if self.get_notice(name=n):
                    self.remove_notice(notice_name=n, flag='create')

                notice = Notices.create(name=n)
        else:
            if self.get_notice(name=name):
                self.remove_notice(notice_name=name, flag='create')

            notice = Notices.create(name=name)

        return notice

    def remove_notice(self, notice_id=None, notice_name=None, flag=None):
        notice = self.get_notice(notice_id, notice_name)
        if notice:
            if flag:
                notice.delete_instance()
            else:
                notice.num = 0
                notice.save()
            return True
        else:
            return False

    def update_notice(self, name=None, num=0):
        if isinstance(name, list) and isinstance(num, list):
            for na, nu in zip(name, num):
                notice = self.get_notice(name=na)
                if notice:
                    notice.num = nu
                    notice.save()

        else:
            notice = self.get_notice(name=name)
            if notice:
                notice.num = num
                notice.save()
                return True
            else:
                return False

    def set_enable(self, notice_name, enable=True):
        notice = self.get_notice(name=notice_name)
        notice.enable = enable
        notice.save()
        return None

    def get_enable(self, notice_name):
        notice = self.get_notice(name=notice_name)
        enable = notice.enable
        return bool(enable)
