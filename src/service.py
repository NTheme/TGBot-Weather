#!/usr/bin/env python3

import os

class SERVICE:
    telegram_token = os.getenv("TG_TOKEN")
    weather_token = os.getenv("WEATHER_TOKEN")
    res = 'share/'
    parse = 'Markdown'
