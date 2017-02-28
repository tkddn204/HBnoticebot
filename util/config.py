#! /bin/env/python
# Operate config file
import configparser

config = configparser.ConfigParser()
config.read('SETTING')
set_config = False
if not config.has_section('credentials'):
    config.add_section('credentials')
    config.set('credentials', 'TOKEN', '')
    config.set('credentials', 'channel_id', '@')
    set_config = True

if not config.has_section('frequency'):
    config.add_section('frequency')
    config.set('frequency', 'when', '10 13 14 19')
    set_config = True

if set_config:
    with open('SETTING', 'a+') as setting:
        config.write(setting)
        setting.close()

TOKEN = config.get('credentials', 'TOKEN')
FREQUENCY = config.get('frequency', 'when')
CHANNEL_ID = config.get('credentials', 'channel_id')
