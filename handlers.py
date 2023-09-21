import random

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

import config
import datas
import keyboards
from config import TOKEN
import parser
from base import DBController

proxy_url = 'http://proxy.server:3128'
bot = Bot(token = TOKEN, proxy=proxy_url)
dp = Dispatcher(bot)
db = DBController(filename=config.botbase_filename)

@dp.message_handler(commands = ['start'])
async def commands(msg: types.Message):
    #await bot.send_sticker(msg.from_user.id, sticker = fr"{random.choice(datas.sticker)}")
    if not db.get_user(msg.from_user.id):
        await bot.send_message(msg.from_user.id, "Ассаламу Алейкум ва Рахматуллохи ва Баракатух 🤝")
        await bot.send_message(msg.from_user.id,
                               "*Выберите свое местоположение 1/2* 👈",
                               parse_mode="Markdown",
                               reply_markup = keyboards.areas)
    else:
        if msg.from_user.id in config.admins_id:
            await bot.send_message(msg.from_user.id, "Ассаламу Алейкум ва Рахматуллохи ва Баракатух 🤝",
                                   reply_markup=keyboards.admin_menu)

        else:
            await bot.send_message(msg.from_user.id, "Ассаламу Алейкум ва Рахматуллохи ва Баракатух 🤝",
                                   reply_markup=keyboards.menu)

        db.update_last_use(msg.from_user.id)


@dp.message_handler()
async def message_command(msg: types.Message):
    user_info = db.get_user(msg.from_user.id)
    if user_info or msg.text == "Команды для Админа 🦸":
        db.update_last_use(msg.from_user.id)
        if msg.text == "Время молитв ⏱":
            try:
                city = user_info[1]
                day = user_info[2]
                time_prayers = parser.time_prayers(city, day)
            except:
                time_prayers = "Ошибка в получении время молитв, пожалуйста сообщите это Администраторам !!!"
                day = "Eror"

            await bot.send_message(msg.from_user.id,
                                   text=time_prayers,
                                   parse_mode="Markdown",
                                   reply_markup=keyboards.day(day)
                                   )

        elif msg.text == "Настройки ⚙":
            await bot.send_message(chat_id=msg.from_user.id,
                                    text="*Настройки:*",
                                    parse_mode="Markdown",
                                    reply_markup=keyboards.settings
                                    )
        elif msg.text == "Команды для Админа 🦸" and msg.from_user.id in config.admins_id:
            await bot.send_message(chat_id=msg.from_user.id,
                                   text="Команды для Админа 🦸",
                                   reply_markup=keyboards.admin_keyboards
                                   )
    else:
        await bot.send_message(msg.from_user.id, "Пожалуйста зарегистрируйтесь сначала...")
        await bot.send_message(msg.from_user.id,
                               "*Выберите свое местоположение 1/2* 👈",
                               parse_mode="Markdown",
                               reply_markup=keyboards.areas)




@dp.callback_query_handler(lambda call: True)
async def callback_buttons(callback_query: types.CallbackQuery):
    try:
        db.update_last_use(callback_query.from_user.id)
    except:
        pass
    user_info = db.get_user(callback_query.from_user.id)

    if not user_info:
        await bot.send_message(callback_query.from_user.id, "Пожалуйста зарегистрируйтесь сначала...")
        await bot.send_message(callback_query.from_user.id,
                               "*Выберите свое местоположение 1/2* 👈",
                               parse_mode="Markdown",
                               reply_markup=keyboards.areas)

    if callback_query.data in datas.all_cities:
        if db.get_user(callback_query.from_user.id):
            db.update_city(callback_query.from_user.id, callback_query.data)

            await bot.edit_message_text(chat_id = callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        text = "*Ваше местоположение успешно изменено !!!* ✅✅✅",
                                        parse_mode="Markdown"
                                        )
        else:
            db.add_user(callback_query.from_user.id, callback_query.data, callback_query.from_user.username)
            await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        text="*Вы успешно зарегистрировались !!!* ✅✅✅",
                                        parse_mode="Markdown"
                                        )

            if callback_query.from_user.id in config.admins_id:
                await bot.send_message(callback_query.from_user.id,
                                       text="*Алхамдулилах*",
                                       parse_mode="Markdown",
                                       reply_markup=keyboards.admin_menu
                                       )
            else:
                await bot.send_message(callback_query.from_user.id,
                                       text="*Алхамдулилах*",
                                       parse_mode="Markdown",
                                       reply_markup=keyboards.menu
                                       )


    elif callback_query.data in ["today", "tomorrow"]:
        edit = True

        if callback_query.data == "today":
            if keyboards.today.text == "Сегодня 🔹":
                edit = False
            else:
                keyboards.today.text = "Сегодня 🔹"
                keyboards.tomorrow.text = "Завтра"
                db.update_day(callback_query.from_user.id, "today")

        else:
            if keyboards.tomorrow.text == "Завтра 🔹":
                edit = False
            else:
                keyboards.today.text = "Сегодня"
                keyboards.tomorrow.text = "Завтра 🔹"
                db.update_day(callback_query.from_user.id, "tomorrow")

        if edit:

            try:
                user_info = db.get_user(callback_query.from_user.id)
                city = user_info[1]
                day = user_info[2]
                time_prayers = parser.time_prayers(city, day)
            except:
                time_prayers = "Ошибка в получении время молитв, пожалуйста сообщите это Администраторам !!!"
                day = "Eror"

            await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                   message_id=callback_query.message.message_id,
                                   text=time_prayers,
                                   parse_mode="Markdown",
                                   reply_markup=keyboards.day(day)
                                   )

    elif callback_query.data in datas.callback_area:
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text="*Выберите свое местоположение 2/2* 👈",
                                    parse_mode="Markdown",
                                    reply_markup=keyboards.cities[datas.callback_area[callback_query.data]]
                                    )

    elif callback_query.data == "Areas":
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text="*Выберите свое местоположение 1/2* 👈",
                                    parse_mode="Markdown",
                                    reply_markup=keyboards.areas
                                    )

    elif callback_query.data == "gps":
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text="*Выберите свое местоположение 1/2* 👈",
                                    parse_mode="Markdown",
                                    reply_markup=keyboards.areas
                                    )

    elif callback_query.data in ["get_users_info", "get_users", "get_base_file"]:
        if callback_query.data == "get_users_info":
            answer = db.get_info_users()
            await bot.send_message(callback_query.from_user.id, answer, parse_mode="html")

        elif callback_query.data == "get_users":
            answer = db.get_users()
            await bot.send_message(callback_query.from_user.id, answer, parse_mode="html")

        elif callback_query.data == "get_base_file":
            await bot.send_document(callback_query.from_user.id, open("botbase.db", "rb"), caption="База данных")
