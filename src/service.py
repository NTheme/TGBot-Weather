#!/usr/bin/env python3

import os
import csv


class SERVICE:
    # os.getenv("TG_TOKEN")
    telegram_token = '6225685870:AAHUk_8qnjnwJsmxGRZUnvNklT80nyhPhfQ'
    # os.getenv("WEATHER_TOKEN")
    weather_token = '63b8fe4d387971a63cabdabd9d1e332f'
    res = 'share/'
    parse = 'Markdown'
    num_files = 4
    data_files = [f'database{i}.csv' for i in range(num_files)]

