#!/usr/bin/env python3

import aiogram


class LINKS:
    github = 'https://github.com/NTheme'
    telegram = 'https://t.me/n_theme'
    source = 'https://openweathermap.org/'
    request = 'http://api.openweathermap.org/data/2.5/forecast/'


class TEXT:
    start = f'Hi! *NThemeWeather* is a weather searcher Telegram bot. '\
            f'Use /help to get more information about usage or just type a city name to find\n\n'\
            f'Author: *NThemeDEV*\n'\
            f'Contacts: {aiogram.utils.markdown.link(url=LINKS.github, title="GitHub")}, '\
            f'{aiogram.utils.markdown.link(url=LINKS.telegram, title="Telegram")}'

    help = f'*---NThemeWeather Bot---*\n\n'\
           f'*What can this bot do?*\n'\
           f'NThemeWeather Bot can give you a full information about weather in any city of the world\n'\
           f'*Commands:*\n'\
           f'  /start - Welcome message\n'\
           f'  /current - Get weather info in last queried city\n'\
           f'  /subscribe - Subscribe to weather notifications'\
           f'  /unsubscribe - Unsubscribe from weather notifications'\
           f'  /help - Bot tips, you are here!\n'\
           f'  /menu - Open a weather menu for a city\n'\
           f'  /exit - Clear city selection (not necessary, you juct may send another one)'\
           f'  /bye - Same as /exit'
    style_ask = f'What period of time for weather do you want?\n'
    response = f'_---Here is the information about the weather---_\n'
    empty = f'Select a city first\n'
    current = f'Current city: '
    set_current = f'Success! Your current city is now set to '
    set_subscribe = f'Success!'
    thanks = f'Not yet, thanks :)'
    source = f'Weather source'
    donate = f'Donate to dev'
    unknown = f'Please, check the city name and try again because we can\'t find a city called '
    exit = f'Bye! :з'
    style_dict = ['Current', 'Tomorrow this time', 'Today per 3 hours', 'Tomorrow per 3 hours', 'Day after per 3 hours',
                  '2 days after per 3 hours', 'Next 5 days this time', 'Set current']
    info = {'city': 'City: ', 'time': 'Date and time: ', 'main': 'Weather condition: ',
            'temp': '  Temperature (in Celsium): ', 'pres': '  Pressure (in MPa): ',
            'hmid': '  Humidity: ', 'skyd': '  Clouds level: ', 'wnds': '  Wind speed: ',
            'wndf': '  Wind direction (in degrees from north): '}

    @staticmethod
    def get_reply(data: dict) -> str:
        reply = ''
        for key, value in data:
            if key != 'city':
                reply += TEXT.info[key] + f'*{str(value)}*\n'
        return reply + '\n'

    @staticmethod
    def is_end_day(time: str) -> bool:
        return time[11:13] == '00'


class SHARE:
    weather_types = {'Clear', 'Clouds', 'Rain',
                     'Snow', 'Thunderstorm', 'Other'}
