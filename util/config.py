#!/bin/env/python
# config file
from configparser import ConfigParser

config = ConfigParser()
config.read('setting.ini')

set_config = False
if not config.has_section('credentials'):
    config.add_section('credentials')
    config.set('credentials', 'token', '')
    config.set('credentials', 'channel_id', '@')

if not config.has_section('frequency'):
    config.add_section('frequency')
    config.set('frequency', 'when', '10 13 16 19')

if set_config:
    with open('SETTING', 'a+') as setting:
        config.write(setting)
        setting.close()

TOKEN = config.get('credentials', 'token')
FREQUENCY = config.get('frequency', 'when')
CHANNEL_ID = config.get('credentials', 'channel_id')
