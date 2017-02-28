# using sqlite3(peewee)
# -*- coding: utf-8 -*-
from db.models import Notices, Users
from db import *


class BotDB:
    def __init__(self):
        db.connect()
        db.create_tables([Notices, Users], safe=True)

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

    # Users
    def get_users(self, user_id=None):
        try:
            if user_id:
                return Users.get(Users.user_id == user_id)
            else:
                return Users.select()
        except Users.DoesNotExist:
            return None

    def get_users_count(self):
        return Users.select().count()

    def get_user_is_set(self, user_id):
        user = self.get_users(user_id)
        if user:
            return user.is_set
        else:
            return None

    def create_users(self, users_id):
        user = Users.create(users_id=users_id)
        return user

    def remove_users(self, users_id):
        user = self.get_users(users_id)
        user.delete_instance()

    def update_users(self, users_id, is_set=False):
        user = self.get_users(users_id)
        if user:
            user.is_set = is_set
            user.save()
            return True
        else:
            return False
