#!/usr/bin/env python3

import aiogram
import src.communicate as communicate

if __name__ == '__main__':
    aiogram.utils.executor.start_polling(communicate.dispatcher)
