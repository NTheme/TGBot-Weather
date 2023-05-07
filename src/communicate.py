#!/usr/bin/env python3

import aiogram
import datetime

from src.service import *
from src.strings import *
from src.request import *

bot = aiogram.Bot(token=SERVICE.telegram_token)
dispatcher = aiogram.Dispatcher(bot=bot)


async def subscribtion():
    now = datetime.datetime.now().hour
    if now != datetime.datetime.now().hour:
        return
    for id, city in user_city.items():
        if city[1] == 0:
            continue
        response = requests.get(LINKS.request, params={
            'q': city[0], 'appid': SERVICE.weather_token})
        if response.status_code != 200:
            continue
        web_request_parse(response, city[0], id)

        user_query = data[id]
        reply = f'{TEXT.response}{TEXT.current}*{user_query[0]["city"]}*\n\n'
        shift = 0
        while not TEXT.is_end_day(user_query[shift]['time']):
            shift += 1
        for index in range(max(0, shift - 8), len(user_query)):
            reply += TEXT.get_reply(user_query[index].items())
            if index + 1 == len(user_query) or TEXT.is_end_day(user_query[index + 1]['time']):
                break

        await bot.send_message(id, reply, parse_mode=SERVICE.parse)


def init():
    for name in SERVICE.data_files:
        if os.path.isfile(name):
            reader = csv.reader(open(name, 'r'), delimiter=',')
            for row in reader:
                user_city[int(row[0])] = [row[1], int(row[2])]
    sch = AsyncIOScheduler(timezone="Europe/Moscow")
    sch.add_job(subscribtion, trigger='interval', seconds=10)
    sch.start()


@dispatcher.message_handler(commands=['start'])
async def cmd_start(msg: aiogram.types.Message):
    buttons = [aiogram.types.InlineKeyboardButton(text=TEXT.source, url=LINKS.source),
               aiogram.types.InlineKeyboardButton(text=TEXT.donate, callback_data='donate')]
    board = aiogram.types.InlineKeyboardMarkup(row_width=2)
    board.add(*buttons)
    await msg.answer_photo(open(SERVICE.res + 'hi.jpg', 'rb'))
    await msg.answer(TEXT.start, parse_mode=SERVICE.parse, disable_web_page_preview=True, reply_markup=board)


@dispatcher.message_handler(commands=['help'])
async def cmd_help(msg: aiogram.types.Message):
    await msg.answer(TEXT.help, parse_mode=SERVICE.parse, disable_web_page_preview=True)


@dispatcher.message_handler(commands=['menu'])
async def cmd_menu(msg: aiogram.types.Message):
    await ask_query_type(msg)


@dispatcher.message_handler(commands=['subscribe'])
async def cmd_subscribe(msg: aiogram.types.Message):
    await change_subscribtion(msg)


@dispatcher.message_handler(commands=['unsubscribe'])
async def cmd_unsubscribe(msg: aiogram.types.Message):
    await change_subscribtion(msg)


@dispatcher.message_handler(commands=['current'])
async def cmd_current(msg: aiogram.types.Message):
    if not msg.from_id in user_city:
        await msg.answer(TEXT.empty, parse_mode=SERVICE.parse)
        return
    await web_request(msg, user_city[msg.from_id][0])


@dispatcher.message_handler(commands=['exit', 'bye'])
async def cmd_exit(msg: aiogram.types.Message):
    if msg.from_id in data:
        data[msg.from_id].clear()
    await msg.answer_photo(open(SERVICE.res + 'bye.jpg', 'rb'), caption=TEXT.exit, parse_mode=SERVICE.parse)


@dispatcher.callback_query_handler(text='donate')
async def button_donate(call: aiogram.types.CallbackQuery):
    await call.message.answer(TEXT.thanks, parse_mode=SERVICE.parse)
    await call.answer()


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('style_'))
async def buttons_menu(call: aiogram.types.CallbackQuery):
    if not call.from_user.id in data or len(data[call.from_user.id]) == 0:
        await call.message.answer(TEXT.empty, parse_mode=SERVICE.parse)
    elif call.data[-1] == '7':
        if not call.from_user.id in user_city:
            user_city[call.from_user.id] = ["", 0]
        user_city[call.from_user.id][0] = data[call.from_user.id][0]["city"]
        writer = csv.writer(
            open(SERVICE.data_files[call.from_user.id % SERVICE.num_files], 'a'), delimiter=',')
        writer.writerow(
            [call.from_user.id, user_city[call.from_user.id][0], user_city[call.from_user.id][1]])
        await call.message.answer(text=f'{TEXT.set_current}*{data[call.from_user.id][0]["city"]}*', parse_mode=SERVICE.parse)
    else:
        await weather_response(call)
    await call.answer()


@dispatcher.message_handler(content_types=['text'])
async def msg_query(msg: aiogram.types.Message):
    await web_request(msg, msg.text)

init()
