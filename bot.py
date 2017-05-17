#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HBHelper made by SsangWoo Han.
from util.config import TOKEN, CHANNEL_ID, FREQUENCY
from util.logger import log
from telegram.ext import Updater
from handlers import Commands, error_handler


# Add handlers
def add_handlers(dp, commands):
    for handler in commands.get_handlers():
        dp.add_handler(handler)
    dp.add_error_handler(error_handler)


def main():
    log.info("HBhelperBot starting...")
    if TOKEN == '':
        log.error('!! TOKEN Don\'t exist... Check your "setting.ini" file!')
        exit()
    elif CHANNEL_ID == ('@' or None or ''):
        log.error('!! CHANNEL_ID Don\'t exist... Check your "setting.ini" file!')
        exit()

    updater = Updater(token=TOKEN)
    dp = updater.dispatcher
    commands = Commands()
    add_handlers(dp, commands)

    if not updater.job_queue.jobs():
        commands.set_alarms(CHANNEL_ID, FREQUENCY.split(" "), updater.job_queue)

    updater.start_polling()
    log.info("Start polling!")
    updater.idle()

if __name__ == '__main__':
    main()
