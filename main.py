from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
import requests
from datetime import datetime
import logging
from config import config

async def main():

    bot = Bot(token=config.token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    dp.message.register(start_bot, Command(commands=['start']))
    dp.message.register(get_weather)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def start_bot(message: Message, bot: Bot):
    await message.answer(f'👋Привіт {message.from_user.username} напиши мені назву міста '
                         f'і дізнайся про актуальну погоду')


key = config.key.get_secret_value()
async def get_weather(message: Message, bot: Bot):
    try:
        city = message.text.lower()
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric&lang=ua')
        data = r.json()

        city = data['name']
        temp = round(data['main']['temp'])
        a = data['weather']
        b = a[0]
        sky = b['description']
        wind = round(data['wind']['speed'])
        day = datetime.now().strftime("%d.%m.%Y")
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime("%H:%M")
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime("%H:%M")

        await message.answer(
                         f'<b>Погода в місті {city} сьогодні ({day}):</b>\n📌температура___ {temp}°C\n📌опади___ '
                         f'{sky}\n📌вітер___ {wind}м/с\n📌схід сонця___ {sunrise}\n📌захід сонця___ {sunset}'
                         )
    except Exception as ex:
        print(ex)
        await message.answer(
            "Ой...Щось пішло не так!\nМожливо помилка в назві міста!?"
        )


if __name__ == "__main__":
    asyncio.run(main())
