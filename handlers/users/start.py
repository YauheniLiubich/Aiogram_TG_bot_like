from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import menu
from loader import dp


# @dp.message_handler(CommandStart(deep_link='start'))
# async def bot_start(message: types.Message):
#     await message.answer(f'Привет, 21634165456!')


# @dp.message_handler(CommandStart(deep_link='start'))
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=menu)
