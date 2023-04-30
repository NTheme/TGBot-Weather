import aiogram
import aiogram.utils.markdown as markdown


class SERVICE:
    telegram_token = '6225685870:AAHUk_8qnjnwJsmxGRZUnvNklT80nyhPhfQ'
    weather_token = '63b8fe4d387971a63cabdabd9d1e332f'
    res = 'share/'
    parse = 'Markdown'


class LINKS:
    github = markdown.link(url='https://github.com/NTheme', title='GitHub')
    telegram = markdown.link(url='https://t.me/n_theme', title='Telegram')
    source = 'https://openweathermap.org/'
    request = 'http://api.openweathermap.org/data/2.5/forecast/'


class TEXT:
    start = f'Hi! *NThemeWeather* is a weather searcher Telegram bot. Use /help to get more information about usage '\
            f'or just type a city name to find\n\n'\
            f'Author: *NThemeDEV*\n'\
            f'Contacts: {LINKS.github}, {LINKS.telegram}'

    help = f'*---NThemeWeather Bot---*\n\n'\
           f'*What can this bot do?*\n'\
           f'NThemeWeather Bot can give you a full information about weather in any city of the world\n'\
           f'*Commands:*\n'\
           f'  /start - Welcome message\n'\
           f'  /help - Bot tips, you are here!\n'\
           f'  /menu - Open a weather menu for a city\n'\
           f'  /exit - Clear city selection (not necessary, you juct may send another one)'\
           f'  /bye - Same as /exit'
    style_ask = f'What period of time for weather do you want?\n'
    response = f'_---Here is the information about the weather---_\n'
    empty = f'Select a city first\n'
    current = f'Current city: '
    thanks = f'Not yet, thanks :)'
    source = f'Weather source'
    donate = f'Donate to dev'
    unknown = f'Please, check the city name and try again because we can\'t find a city called '
    exit = f'Bye! :з'
    style_dict = ['Current', 'Tomorrow this time', 'Today per 3 hours', 'Tomorrow per 3 hours', 'Day after per 3 hours',
                  '2 days after per 3 hours', 'Next 5 days this time']
    info = {'city': 'City: ', 'time': 'Date and time: ', 'main': 'Weather condition: ',
            'temp': '  Temperature (in Celsium): ', 'pres': '  Pressure (in MPa): ',
            'hmid': '  Humidity: ', 'skyd': '  Clouds level: ', 'wnds': '  Wind speed: ',
            'wndf': '  Wind direction (in degrees from north): '}


class SHARE:
    weather_types = {'Clear', 'Clouds', 'Rain',
                     'Snow', 'Thunderstorm', 'Other'}
