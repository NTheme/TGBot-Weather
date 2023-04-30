#!/usr/bin/env python3

import src.communicate as communicate
import aiogram

if __name__ == '__main__':
    aiogram.utils.executor.start_polling(communicate.dispatcher)
