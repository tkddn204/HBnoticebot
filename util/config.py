#! /bin/env/python
# Operate config file
import configparser

config = configparser.ConfigParser()
config.read('SETTING')
if not config.has_section('credentials'):
    config.add_section('credentials')
    config.set('credentials', 'TOKEN', '')
    with open('SETTING', 'a+') as setting:
        config.write(setting)
        setting.close()
if not config.has_section('configs'):
    config.add_section('configs')
    config.set('configs', 'TODO_LIMIT', '30')
    with open('SETTING', 'a+') as setting:
        config.write(setting)
        setting.close()

TOKEN = config.get('credentials', 'TOKEN')
TODO_LIMIT = config.get('configs', 'TODO_LIMIT')
