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
from util.config import FREQUENCY, CHANNEL_ID
from crawling import get_notice, get_all_notice


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
            CommandHandler('new', self.command_new),
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

    def view_update(self, bot, job=None, channel_id=None):
        if job:
            channel_id = job.context
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
                    bot.sendMessage(channel_id,
                                    text=export,
                                    disable_notification=True,
                                    parse_mode=ParseMode.HTML)
                else:
                    not_export += 1

        if not_export < len(FIND_THINGS):
            return bot.sendMessage(channel_id,
                                   text=NEW_NOTICE,
                                   parse_mode=ParseMode.HTML)

    def set_alarms(self, channel_id, when, job_queue):
        for w in when:
            job_queue.run_daily(self.view_update, datetime.time(hour=int(w)),
                                days=tuple(range(5)),
                                context=channel_id,
                                name='{0} {1}'.format(channel_id, w))

    def command_new(self, bot, update):
        self.view_update(bot, channel_id=CHANNEL_ID)

    def command_set(self, bot, update, job_queue):
        channel_id = CHANNEL_ID
        when = FREQUENCY.split(' ')
        self.set_alarms(channel_id, when, job_queue)
        text = ''
        for w in when:
            text += w + '시, '
        return bot.sendMessage(
            update.message.chat_id,
            text=SET_ALARM.format(text[:-2]))

    def command_unset(self, bot, update, job_queue):
        if job_queue.jobs:
            job_queue.stop()
            bot.sendMessage(update.message.chat_id,
                            text=UNSET_ALARM)

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
