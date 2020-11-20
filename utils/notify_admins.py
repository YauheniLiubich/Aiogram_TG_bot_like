import logging

from aiogram import Dispatcher

from data.config import admins



async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")
            bot_user = await dp.bot.get_me()

        except Exception as err:
            logging.exception(err)


