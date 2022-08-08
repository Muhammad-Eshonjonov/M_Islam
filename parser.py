import requests
import datetime
import config
from requests import get
from bs4 import BeautifulSoup as BS

date_now = datetime.date.today()
cities_time = {
    "Душанбе":0,
    "Айни":5,
    "Ашт":-9,
    "Бохтар (Кургонтеппа)":4,
    "Бустон":-7,
    "Вахдат":0,
    "Истаравшан":-5,
    "Исфара":-9,
    "Конибодом":-9,
    "Кулоб":-5,
    "Мургоб":-20,
    "Норак":-4,
    "Панчакент":5,
    "Рашт":-7,
    "Турсунзода":0,
    "Хисор":0,
    "Хоруг":-12,
    "Хучанд":-7,
    "Шахритус":5
}

def parsing_times(day):
    url = 'http://shuroiulamo.tj/tj/namaz'
    r = requests.get(url)
    html = BS(r.content, 'lxml')

    if day == "today": # собирание время молитв на сегодня
        trs_today = html.find('tr', class_='today')
        tds_today = trs_today.find_all('td')
        today_data_melodi = tds_today[1]
        today_data_hijri = tds_today[2]
        fajr_today_minute = int(tds_today[3].text[0] + tds_today[3].text[1]) * 60 + int(
            tds_today[3].text[3] + tds_today[3].text[4])
        zuhr_today_minute = int(tds_today[4].text[0] + tds_today[4].text[1]) * 60 + int(
            tds_today[4].text[3] + tds_today[4].text[4])
        asr_today_minute = int(tds_today[5].text[0] + tds_today[5].text[1]) * 60 + int(
            tds_today[5].text[3] + tds_today[5].text[4])
        magrib_today_minute = int(tds_today[7].text[0] + tds_today[7].text[1]) * 60 + int(
            tds_today[7].text[3] + tds_today[7].text[4])
        isha_today_minute = int(tds_today[8].text[0] + tds_today[8].text[1]) * 60 + int(
            tds_today[8].text[3] + tds_today[8].text[4])

        return today_data_melodi, today_data_hijri, fajr_today_minute, zuhr_today_minute, asr_today_minute, magrib_today_minute, isha_today_minute

    elif day == "tomorrow": # собирание время молитв на завтра
        trs_tomorrow = html.find_all('tr', class_='')[1]
        tds_tomorrow = trs_tomorrow.find_all('td')
        tomorrow_data_melodi = tds_tomorrow[1]
        tomorrow_data_hijri = tds_tomorrow[2]
        fajr_tomorrow_minute = int(tds_tomorrow[3].text[0] + tds_tomorrow[3].text[1]) * 60 + int(
            tds_tomorrow[3].text[3] + tds_tomorrow[3].text[4])
        zuhr_tomorrow_minute = int(tds_tomorrow[4].text[0] + tds_tomorrow[4].text[1]) * 60 + int(
            tds_tomorrow[4].text[3] + tds_tomorrow[4].text[4])
        asr_tomorrow_minute = int(tds_tomorrow[5].text[0] + tds_tomorrow[5].text[1]) * 60 + int(
            tds_tomorrow[5].text[3] + tds_tomorrow[5].text[4])
        magrib_tomorrow_minute = int(tds_tomorrow[7].text[0] + tds_tomorrow[7].text[1]) * 60 + int(
            tds_tomorrow[7].text[3] + tds_tomorrow[7].text[4])
        isha_tomorrow_minute = int(tds_tomorrow[8].text[0] + tds_tomorrow[8].text[1]) * 60 + int(
            tds_tomorrow[8].text[3] + tds_tomorrow[8].text[4])

        return tomorrow_data_melodi, tomorrow_data_hijri, fajr_tomorrow_minute, zuhr_tomorrow_minute, asr_tomorrow_minute, magrib_tomorrow_minute, isha_tomorrow_minute

def time_prayers(city, day):
    if day == "today":
        times = parsing_times("today")
        data_melodi = times[0].text
        data_hijri = times[1].text

        fajr = times[2] + cities_time[city]
        fajr_text = '0' * (2 - len(str(fajr // 60))) + str(fajr // 60) + ":" + '0' * (2 - len(str(fajr % 60))) + str(fajr % 60)

        zuhr = times[3] + cities_time[city]
        zuhr_text = '0' * (2 - len(str(zuhr // 60))) + str(zuhr // 60) + ":" + '0' * (2 - len(str(zuhr % 60))) + str(zuhr % 60)

        asr = times[4] + cities_time[city]
        asr_text = '0' * (2 - len(str(asr // 60))) + str(asr // 60) + ":" + '0' * (2 - len(str(asr % 60))) + str(asr % 60)

        magrib = times[5] + cities_time[city]
        magrib_text = '0' * (2 - len(str(magrib // 60))) + str(magrib // 60) + ":" + '0' * (2 - len(str(magrib % 60))) + str(magrib % 60)

        isha = times[6] + cities_time[city]
        isha_text = '0' * (2 - len(str(isha // 60))) + str(isha // 60) + ":" + '0' * (2 - len(str(isha % 60))) + str(isha % 60)

        answer = fr"""_
Время молитв для города {city} на сегодня
{data_melodi}
({data_hijri})_
*
Фаджр:           {fajr_text}
Зухр:               {zuhr_text}
Аср:                 {asr_text}
Магриб:         {magrib_text}
Иша:               {isha_text}

@{config.username_bot}*
"""

    elif day == "tomorrow":
        times = parsing_times("tomorrow")
        data_melodi = times[0].text
        data_hijri = times[1].text

        fajr = times[2] + cities_time[city]
        fajr_text = '0' * (2 - len(str(fajr // 60))) + str(fajr // 60) + ":" + '0' * (2 - len(str(fajr % 60))) + str(fajr % 60)

        zuhr = times[3] + cities_time[city]
        zuhr_text = '0' * (2 - len(str(zuhr // 60))) + str(zuhr // 60) + ":" + '0' * (2 - len(str(zuhr % 60))) + str(zuhr % 60)

        asr = times[4] + cities_time[city]
        asr_text = '0' * (2 - len(str(asr // 60))) + str(asr // 60) + ":" + '0' * (2 - len(str(asr % 60))) + str(asr % 60)

        magrib = times[5] + cities_time[city]
        magrib_text = '0' * (2 - len(str(magrib // 60))) + str(magrib // 60) + ":" + '0' * (2 - len(str(magrib % 60))) + str(magrib % 60)

        isha = times[6] + cities_time[city]
        isha_text = '0' * (2 - len(str(isha // 60))) + str(isha // 60) + ":" + '0' * (2 - len(str(isha % 60))) + str(isha % 60)

        answer = fr"""_
Время молитв для города {city} на завтра
{data_melodi}
({data_hijri})_
*
Фаджр:           {fajr_text}
Зухр:               {zuhr_text}
Аср:                 {asr_text}
Магриб:         {magrib_text}
Иша:               {isha_text}

@{config.username_bot}*
"""

    else:
        answer = "Ошибка выбора даты"

    return answer