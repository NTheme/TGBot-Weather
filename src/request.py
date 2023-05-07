#!/usr/bin/env python3

import requests
import aiogram
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.service import *
from src.strings import *

user_city = dict()
data = dict(list(dict()))


async def weather_response(call: aiogram.types.CallbackQuery):
    user_query = data[call.from_user.id]
    type = int(call.data[-1])
    reply = f'{TEXT.response}{TEXT.current}*{user_query[0]["city"]}*\n\n'
    if type < 2:
        reply += TEXT.get_reply(user_query[type * 8].items())
        img_name = user_query[type * 8]['main'].lower()
        if user_query[type * 8]['main'] == 'Clear':
            if 9 <= int(user_query[type * 8]['time'][11:13]) <= 18:
                img_name = 'day'
            else:
                img_name = 'night'
        await call.message.answer_photo(open(SERVICE.res + img_name + '.jpg', 'rb'))
    elif type < 6:
        shift = 0
        while not TEXT.is_end_day(user_query[shift]['time']):
            shift += 1
        for index in range(max(0, shift + (type - 3) * 8), len(user_query)):
            reply += TEXT.get_reply(user_query[index].items())
            if index + 1 == len(user_query) or TEXT.is_end_day(user_query[index + 1]['time']):
                break
    elif type < 7:
        for i in range(len(user_query) // 8):
            reply += TEXT.get_reply(user_query[i * 8].items())

    await call.message.answer(text=reply, parse_mode=SERVICE.parse)
    await call.answer()


def web_request_parse(response: requests.Response, city: str, id: int):
    query = response.json()["list"]
    global data
    data[id] = [dict() for i in range(len(query))]

    for i in range(len(query)):
        current = data[id][i]
        current['city'] = city[0].upper() + city[1:]
        current['time'] = query[i]["dt_txt"]
        current['main'] = query[i]["weather"][0]["main"]
        current['temp'] = round(query[i]["main"]["temp"] - 273.15, 1)
        current['pres'] = query[i]["main"]["pressure"]
        current['hmid'] = query[i]["main"]["humidity"]
        current['skyd'] = query[i]["clouds"]["all"]
        current['wnds'] = query[i]["wind"]["speed"]
        current['wndf'] = query[i]["wind"]["deg"]


async def web_request(msg: aiogram.types.Message, city: str):
    response = requests.get(LINKS.request, params={
        'q': city.lower(), 'appid': SERVICE.weather_token})
    if response.status_code != 200:
        reply = TEXT.unknown + msg.text
        await msg.reply(reply, parse_mode=SERVICE.parse)
    else:
        web_request_parse(response, city, msg.from_id)
        await ask_query_type(msg)


async def ask_query_type(msg: aiogram.types.Message):
    if not msg.from_id in data or len(data[msg.from_id]) == 0:
        await msg.answer(TEXT.empty, parse_mode=SERVICE.parse)
        return
    buttons = [aiogram.types.InlineKeyboardButton(
        text=TEXT.style_dict[i], callback_data=f'style_{i}') for i in range(len(TEXT.style_dict))]
    board = aiogram.types.InlineKeyboardMarkup(row_width=2)
    board.add(*buttons)
    await msg.answer(f'{TEXT.style_ask}{TEXT.current}*{data[msg.from_id][0]["city"]}*\n',
                     parse_mode=SERVICE.parse, disable_web_page_preview=True, reply_markup=board)


async def change_subscribtion(msg: aiogram.types.Message):
    if not msg.from_id in user_city:
        await msg.answer(TEXT.empty, parse_mode=SERVICE.parse)
        return
    type = 1 if msg.text == '/subscribe' else 0
    user_city[msg.from_id][1] = type
    writer = csv.writer(
        open(SERVICE.data_files[msg.from_id % SERVICE.num_files], 'a'), delimiter=',')
    writer.writerow([msg.from_id, user_city[msg.from_id][0], type])
    await msg.answer(TEXT.set_subscribe, parse_mode=SERVICE.parse)
