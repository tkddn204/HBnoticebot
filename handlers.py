# Bot's Operation
# -*- coding: utf-8 -*-
from telegram import InlineKeyboardMarkup, \
    InlineQueryResultArticle, InputTextMessageContent, ParseMode, \
    ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, \
    InlineQueryHandler, CallbackQueryHandler, Job

from util.logger import log
from db.models import Notice
from text import *
from crawling import get_notice


# Error! WYEEEEEEEE---
def error_handler(bot, update, err):
    log.error('!! Update %s :: \n %s' % (update, err))


class WithDB:
    def __init__(self):
        self.db = Notice()


class Commands(WithDB):
    def __init__(self):
        WithDB.__init__(self)
        self.handlers = [
            CommandHandler('start', self.command_start, pass_args=True),
            CommandHandler('help', self.command_help),
            MessageHandler(Filters.text, self.messages, pass_job_queue=True)
        ]

    def command_start(self, bot, update, args):
        user_name = update.message.from_user.first_name

        if len(args) < 1:
            bot.sendMessage(
                update.message.chat_id,
                text=(START.format(bot_name=bot.name,
                                   user_name=user_name)),
                reply_markup=ReplyKeyboardMarkup(
                    LIST_KEYBOARD))

    def command_help(self, bot, update):
        bot.sendMessage(
            update.message.chat_id,
            text=HELP.format(
                bot_name=bot.name),
            reply_markup=ReplyKeyboardMarkup(LIST_KEYBOARD))

    def messages(self, bot, update, job_queue):
        text = update.message.text

        export = ''
        (notices, urls) = get_notice(text)
        for i in range(len(notices)):
            export += ('<a href="{0}">'.format(urls[i]) + notices[i] + '</a>\n')
        bot.sendMessage(update.message.chat_id,
                        text=export,
                        parse_mode=ParseMode.HTML)

    def get_handlers(self):
        return self.handlers

