# Bot's Operation
# -*- coding: utf-8 -*-
import datetime
from telegram import ParseMode, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters

from util.logger import log
from db.db import BotDB
from text import *
from util.config import FREQUENCY, CHANNEL_ID
from crawling import get_notice, get_all_notice


# Error! WYEEEEEEEE---
def error_handler(bot, update, err):
    if update:
        log.error('!! Update %s :: %s' % (update, err))


class WithDB:
    def __init__(self):
        self.db = BotDB()


class Commands(WithDB):
    def __init__(self):
        WithDB.__init__(self)
        self.handlers = [
            CommandHandler('start', self.command_start),
            CommandHandler('help', self.command_help),
            CommandHandler('new', self.command_new),
            CommandHandler('set', self.command_set, pass_job_queue=True),
            CommandHandler('unset', self.command_unset, pass_job_queue=True),
            CommandHandler('setting', self.command_setting, pass_args=True),
            MessageHandler(Filters.text, self.messages)
        ]

    def command_start(self, bot, update):
        user_name = update.message.from_user.first_name

        return bot.sendMessage(
            update.message.chat_id,
            text=START.format(bot_name=bot.name, user_name=user_name),
            reply_markup=ReplyKeyboardMarkup(LIST_KEYBOARD))

    def command_help(self, bot, update):
        return bot.sendMessage(
            update.message.chat_id,
            text=HELP,
            reply_markup=ReplyKeyboardMarkup(LIST_KEYBOARD))

    def __check_more_than_max_numbers_of_find_things(self):
        notice_dict, notice_max_dict = get_all_notice()
        if not self.db.get_notice():
            self.db.create_notice(FIND_THINGS)

        result = {}
        for find_things in FIND_THINGS:
            current_db_notice_num = self.db.get_notice(name=find_things).num
            result[find_things] = []
            for notice in notice_dict[find_things]:
                if notice['num'] > current_db_notice_num:
                    result[find_things].append(notice)

        self.db.update_notice(notice_max_dict)
        return result

    def __view_update(self, bot, job):
        channel_id = job if isinstance(job, str) else job.context
        result = self.__check_more_than_max_numbers_of_find_things()
        last_message = ''
        for find_thing in FIND_THINGS:
            if result[find_thing]:
                export_message = '--- {0} ---\n'.format(find_thing)
                count = 0
                for notice in result[find_thing]:
                    count += 1
                    export_message += '{title}(<a href="{url}">링크</a>)\n'\
                        .format(title=notice['title'], url=notice['url'])
                bot.sendMessage(channel_id,
                                text=export_message,
                                disable_notification=True,
                                parse_mode=ParseMode.HTML)

                last_message += '{0}({1}개)/'.format(find_thing, count)

        if last_message:
            message_text = last_message[:-1]
            bot.sendMessage(channel_id,
                            text=NEW_NOTICE+message_text,
                            parse_mode=ParseMode.HTML)
        else:
            message_text = '공지사항 없음'

        log.info(message_text)

    def set_alarms(self, channel_id, when, job_queue):
        for w in when:
            job_queue.run_daily(self.__view_update, datetime.time(hour=int(w)),
                                days=tuple(range(5)),
                                context=channel_id,
                                name='{0} {1}'.format(channel_id, w))

    def command_new(self, bot, update):
        log.info('[/new] get notice list')
        self.__view_update(bot, job=CHANNEL_ID)

    def command_set(self, bot, update, job_queue):
        channel_id = CHANNEL_ID
        when = FREQUENCY.split(' ')
        self.set_alarms(channel_id, when, job_queue)
        text = ''
        for w in when:
            text += '{0}시, '.format(w)
        log.info('[/set] {0}'.format(SET_ALARM.format(text[:-2])))
        return bot.sendMessage(
            update.message.chat_id,
            text=SET_ALARM.format(text[:-2]))

    def command_unset(self, bot, update, job_queue):
        if job_queue.jobs:
            job_queue.stop()
            log.info('[/unset] {0}'.format(UNSET_ALARM))
            bot.sendMessage(update.message.chat_id,
                            text=UNSET_ALARM)

    def command_setting(self, bot, update, args):
        if len(args) < 1:
            return bot.sendMessage(
                update.message.chat_id,
                text=TEXT_NOT_INPUT)
        elif args[0] in FIND_THINGS:
            enable = not self.db.get_enable(args[0])
            self.db.set_enable(args[0], enable)
            log.info('[/setting] {0} {1} '.format(args[0], TEXT_DONE.format(enable)))
            return bot.sendMessage(
                update.message.chat_id,
                text=TEXT_DONE.format(enable))

    def command_close(self, bot, update, args):
        if len(args) < 1:
            return bot.sendMessage(
                update.message.chat_id,
                text=TEXT_NOT_INPUT)
        elif args[0] in FIND_THINGS:
            self.db.set_enable(args[0], False)
            log.info('[/close] {0} {1} '.format(args[0], TEXT_DONE.format(False)))
            return bot.sendMessage(
                update.message.chat_id,
                text=TEXT_DONE.format(False))

    def messages(self, bot, update):
        if not update.message.text:
            self.command_help(bot, update)
            return
        else:
            text = update.message.text

        if text in FIND_THINGS:
            if self.db.get_enable(text):
                export_message = ''
                notice, max_num = get_notice(text)
                for post in notice:
                    export_message += '{0}(<a href="{1}">링크</a>)\n'.format(post['title'], post['url'])
                log.info('[{0}] {1}({2})님이 {3}개 요청'.format(text,
                                                           update.message.from_user.first_name,
                                                           update.message.chat_id,
                                                           len(notice)))
                return bot.sendMessage(update.message.chat_id,
                                       text=export_message,
                                       parse_mode=ParseMode.HTML)
            else:
                return bot.sendMessage(update.message.chat_id,
                                       text=TEXT_CLOSE,
                                       parse_mode=ParseMode.HTML)

    def get_handlers(self):
        return self.handlers
