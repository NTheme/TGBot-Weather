#!/usr/bin/env python3

import aiogram
import requests
from src.service import *
from src.strings import *

bot = aiogram.Bot(token=SERVICE.telegram_token)
dispatcher = aiogram.Dispatcher(bot=bot)
data = dict(list(dict()))


@dispatcher.message_handler(commands=['start'])
async def cmd_start(msg: aiogram.types.Message):
    buttons = [aiogram.types.InlineKeyboardButton(text=TEXT.source, url=LINKS.source),
               aiogram.types.InlineKeyboardButton(text=TEXT.donate, callback_data='donate')]
    board = aiogram.types.InlineKeyboardMarkup(row_width=2)
    board.add(*buttons)
    await msg.answer_photo(open(SERVICE.res + 'hi.jpg', 'rb'))
    await msg.answer(TEXT.start, parse_mode=SERVICE.parse, disable_web_page_preview=True, reply_markup=board)


@dispatcher.callback_query_handler(text='donate')
async def button_donate(call: aiogram.types.CallbackQuery):
    await call.message.answer(TEXT.thanks, parse_mode=SERVICE.parse)
    await call.answer()


@dispatcher.message_handler(commands=['help'])
async def cmd_help(msg: aiogram.types.Message):
    await msg.answer(TEXT.help, parse_mode=SERVICE.parse, disable_web_page_preview=True)


@dispatcher.message_handler(commands=['menu'])
async def cmd_menu(msg: aiogram.types.Message):
    await get_weather_type(msg)


@dispatcher.message_handler(commands=['exit', 'bye'])
async def cmd_exit(msg: aiogram.types.Message):
    if msg.from_id in data:
        data[msg.from_id].clear()
    await msg.answer_photo(open(SERVICE.res + 'bye.jpg', 'rb'), caption=TEXT.exit, parse_mode=SERVICE.parse)


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('style_'))
async def menu_parser(call: aiogram.types.CallbackQuery):
    user_base = data[call.from_user.id]
    if not call.from_user.id in data or len(user_base) == 0:
        await call.message.answer(TEXT.empty, parse_mode=SERVICE.parse)
        return

    type = int(call.data[-1])
    reply = f'{TEXT.response}{TEXT.current}*{user_base[0]["city"]}*\n\n'
    if type < 2:
        reply += TEXT.get_reply(user_base[type * 8].items())
        img_name = user_base[type * 8]['main'].lower()
        if user_base[type * 8]['main'] == 'Clear':
            if 9 <= int(user_base[type * 8]['time'][11:13]) <= 18:
                img_name = 'day'
            else:
                img_name = 'night'
        await call.message.answer_photo(open(SERVICE.res + img_name + '.jpg', 'rb'))
    elif type < 6:
        shift = 0
        while not TEXT.is_end_day(user_base[shift]['time']):
            shift += 1
        for index in range(max(0, shift + (type - 3) * 8), len(user_base)):
            reply += TEXT.get_reply(user_base[index].items())
            if index + 1 == len(user_base) or TEXT.is_end_day(user_base[index + 1]['time']):
                break
    else:
        for i in range(len(user_base) // 8):
            reply += TEXT.get_reply(user_base[i * 8].items())

    await call.message.answer(text=reply, parse_mode=SERVICE.parse)
    await call.answer()


@dispatcher.message_handler(content_types=['text'])
async def get_city(msg: aiogram.types.Message):
    response = requests.get(LINKS.request, params={
        'q': msg.text.lower(), 'appid': SERVICE.weather_token})
    if response.status_code != 200:
        reply = TEXT.unknown + msg.text
        await msg.reply(reply, parse_mode=SERVICE.parse)
    else:
        base = response.json()["list"]
        global data
        data[msg.from_id] = [dict() for i in range(len(base))]
        for i in range(len(base)):
            data[msg.from_id][i]['city'] = msg.text[0].upper() + msg.text[1:]
            data[msg.from_id][i]['time'] = base[i]["dt_txt"]
            data[msg.from_id][i]['main'] = base[i]["weather"][0]["main"]
            data[msg.from_id][i]['temp'] = round(
                base[i]["main"]["temp"] - 273.15, 1)
            data[msg.from_id][i]['pres'] = base[i]["main"]["pressure"]
            data[msg.from_id][i]['hmid'] = base[i]["main"]["humidity"]
            data[msg.from_id][i]['skyd'] = base[i]["clouds"]["all"]
            data[msg.from_id][i]['wnds'] = base[i]["wind"]["speed"]
            data[msg.from_id][i]['wndf'] = base[i]["wind"]["deg"]

        await get_weather_type(msg)


async def get_weather_type(msg: aiogram.types.Message):
    if not msg.from_id in data or len(data[msg.from_id]) == 0:
        await msg.answer(TEXT.empty, parse_mode=SERVICE.parse)
        return
    buttons = [aiogram.types.InlineKeyboardButton(
        text=TEXT.style_dict[i], callback_data=f'style_{i}') for i in range(len(TEXT.style_dict))]
    board = aiogram.types.InlineKeyboardMarkup(row_width=2)
    board.add(*buttons)
    await msg.answer(f'{TEXT.style_ask}{TEXT.current}*{data[msg.from_id][0]["city"]}*\n',
                     parse_mode=SERVICE.parse, disable_web_page_preview=True, reply_markup=board)
