from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import datas

menu = ReplyKeyboardMarkup(
    resize_keyboard = True, one_time_keyboard = False
)

menu.row(KeyboardButton('Время молитв ⏱'), KeyboardButton('Настройки ⚙'))

areas = InlineKeyboardMarkup()
for area in datas.areas:
    areas.row(InlineKeyboardButton(area, callback_data=datas.area_callback[area]))

cities = {}
for area in datas.areas:
    cities[area] = InlineKeyboardMarkup()
    for city in datas.cities[area]:
        cities[area].row(InlineKeyboardButton(city, callback_data=city))

    cities[area].row(InlineKeyboardButton("Назад 🔙", callback_data="Areas"))


today = InlineKeyboardButton("Сегодня 🔹", callback_data = "today")
tomorrow = InlineKeyboardButton("Завтра", callback_data = "tomorrow")

def day(day):
    if day == "today":
        today.text = "Сегодня 🔹"
        tomorrow.text = "Завтра"
    elif day == "tomorrow":
        today.text = "Сегодня"
        tomorrow.text = "Завтра 🔹"

    else:
        today.text = "Сегодня"
        tomorrow.text = "Завтра"

    day = InlineKeyboardMarkup().row(today, tomorrow)

    return day

settings = InlineKeyboardMarkup().row(InlineKeyboardButton("Изменить местоположение", callback_data="gps"))

admin_keyboards = InlineKeyboardMarkup()
admin_keyboards.row(InlineKeyboardButton("Пользователы (с инфо)", callback_data="get_users_info"),
                    InlineKeyboardButton("Пользователы (без инфо)", callback_data="get_users"))

admin_keyboards.row(InlineKeyboardButton("База данных (файл)", callback_data="get_base_file"))

admin_menu = ReplyKeyboardMarkup(
    resize_keyboard = True, one_time_keyboard = False
)

admin_menu.row(KeyboardButton('Время молитв ⏱'), KeyboardButton('Настройки ⚙')).row(KeyboardButton('Команды для Админа 🦸'))