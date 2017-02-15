#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HBHelper made by SsangWoo Han.
import sys
from util.config import TOKEN
from util.logger import log
from telegram.ext import Updater
from handlers import Commands, error_handler


# Add handlers
def add_handlers(dp):
    for handler in Commands().get_handlers():
        dp.add_handler(handler)
    dp.add_error_handler(error_handler)


def main():
    log.info("HBhelperBot starting...")
    if TOKEN == '':
        log.error('!! TOKEN Don\'t exist... Check your "SETTING" file!')
        sys.exit()
    updater = Updater(token=TOKEN)
    dp = updater.dispatcher
    add_handlers(dp)

    updater.start_polling()
    log.info("Start polling!")
    updater.idle()

if __name__ == '__main__':
    main()
