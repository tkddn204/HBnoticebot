#! /bin/env/python
# Operate config file
import configparser

config = configparser.ConfigParser()
config.read('SETTING')
set_config = False
if not config.has_section('credentials'):
    config.add_section('credentials')
    config.set('credentials', 'TOKEN', '')
    set_config = True

if set_config:
    with open('SETTING', 'a+') as setting:
        config.write(setting)
        setting.close()

TOKEN = config.get('credentials', 'TOKEN')
