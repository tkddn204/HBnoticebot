# Bot's Operation
# -*- coding: utf-8 -*-
import datetime
from telegram import InlineKeyboardMarkup, \
    InlineQueryResultArticle, InputTextMessageContent, ParseMode, \
    ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, \
    InlineQueryHandler, CallbackQueryHandler

from util.logger import log
from db.db import BotDB
from text import *
from crawling import get_notice, get_all_notice, get_max_of_find_things


# Error! WYEEEEEEEE---
def error_handler(bot, update, err):
    log.error('!! Update %s :: \n %s' % (update, err))


class WithDB:
    def __init__(self):
        self.db = BotDB()


class Commands(WithDB):
    def __init__(self):
        WithDB.__init__(self)
        self.handlers = [
            CommandHandler('start', self.command_start),
            CommandHandler('help', self.command_help),
            CommandHandler('set', self.command_set, pass_job_queue=True),
            CommandHandler('unset', self.command_unset, pass_job_queue=True),
            MessageHandler(Filters.text, self.messages)
        ]

    def command_start(self, bot, update):
        user_name = update.message.from_user.first_name

        return bot.sendMessage(
            update.message.chat_id,
            text=(START.format(bot_name=bot.name, user_name=user_name)),
            reply_markup=ReplyKeyboardMarkup(LIST_KEYBOARD))

    def command_help(self, bot, update):
        return bot.sendMessage(
            update.message.chat_id,
            text=HELP,
            reply_markup=ReplyKeyboardMarkup(LIST_KEYBOARD))

    def check_find_things(self):
        find_list = get_all_notice()
        max_list = []
        for find_things in FIND_THINGS:
            max_list.append(find_list[find_things]['max'])
        if not self.db.get_notice():
            self.db.create_notice(FIND_THINGS)

        result = {}
        for find_things in FIND_THINGS:
            notice = self.db.get_notice(name=find_things)
            result[find_things] = {'name': [], 'url': []}
            for count in range(len(find_list[find_things]['name'])):
                if find_list[find_things]['num'][count] > notice.num:
                    result[find_things]['name'].append(find_list[find_things]['name'][count])
                    result[find_things]['url'].append(find_list[find_things]['url'][count])

        self.db.update_notice(FIND_THINGS, max_list)
        return result

    def alarm(self, bot, job):
        not_export = 0
        result = self.check_find_things()
        for find_things in FIND_THINGS:
            if result[find_things]:
                export = find_things + ' \n'
                for i in range(len(result[find_things]['name'])):
                    name = result[find_things]['name'][i]
                    url = result[find_things]['url'][i]
                    export += (name + '(' + '<a href="{0}">'.format(url) + '링크' + '</a>)\n')
                if export != find_things + ' \n':
                    bot.sendMessage(job.context,
                                    text=export,
                                    parse_mode=ParseMode.HTML)
                else:
                    not_export += 1
        if not_export >= len(FIND_THINGS):
            bot.sendMessage(job.context,
                            text='오늘은 업데이트 내역이 없습니다!',
                            parse_mode=ParseMode.HTML)

    def set_alarms(self, user_id, job_queue):
        job_queue.run_once(self.alarm, datetime.timedelta(seconds=10),
                            context=user_id,
                            name='{} 10'.format(user_id))
# days=tuple(range(5)),
    def command_set(self, bot, update, job_queue):
        user_id = update.message.from_user.id
        self.set_alarms(user_id, job_queue)

        return bot.sendMessage(
            update.message.chat_id,
            text=SET)

    def command_unset(self, bot, update, job_queue):
        pass

    def messages(self, bot, update):
        text = update.message.text

        export = ''
        (notices, urls) = get_notice(text)
        for i in range(len(notices)):
            export += ('<a href="{0}">'.format(urls[i]) + notices[i] + '</a>\n')
        return bot.sendMessage(update.message.chat_id,
                               text=export,
                               parse_mode=ParseMode.HTML)

    def get_handlers(self):
        return self.handlers

