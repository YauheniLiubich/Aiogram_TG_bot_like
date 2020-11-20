import logging

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import channels, channels_comment_id, bot_name, name_discussion_group
from handlers.channels.func import send
from keyboards.inline.callback_data import like_callback
from loader import dp, bot
from utils.db_api import quick_commands as commands


@dp.message_handler(content_types=types.ContentTypes.ANY, chat_id=channels_comment_id)
async def get_m_id(message):

    # id_message = message.message_id
    message_id = message.forward_from_message_id
    try:
        if message.forward_from_chat.id == channels[0]:
            await commands.add_post(post_id=message_id)
            m_id = message.message_id
            text = message.text
            message_id = message.forward_from_message_id
            like_list = await commands.get_like_condition(post_id=message_id)
            rating_keyboard2 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=f"🔥 {like_list[1]}",
                                             callback_data=like_callback.new(action='no_reaction')),
                        InlineKeyboardButton(text=f"👍 {like_list[0]}",
                                             callback_data=like_callback.new(action='up_like')),
                        InlineKeyboardButton(text=f"👎 {like_list[2]}",
                                             callback_data=like_callback.new(action='down_like'))
                    ],
                    [
                        InlineKeyboardButton(text='Предложить новость', url=f'http://t.me/{bot_name}?start=start'),
                        InlineKeyboardButton(text='Прокомментировать',
                                             url=f'http://t.me/{name_discussion_group}/{m_id}?comment=1'),
                    ]
                ]

            )
            await bot.edit_message_reply_markup(chat_id=channels[0], message_id=message_id,
                                                reply_markup=rating_keyboard2)
            # await bot.send_message(chat_id=channels_comment_id, text=' 👆  👆  👆  👆  👆  👆  👆  👆  👆  👆  👆 ', reply_to_message_id=message.message_id, reply_markup=rating_keyboard2)
            # await message.send_copy(chat_id=-1001101661839, reply_markup=rating_keyboard2)

            if message.content_type == 'photo':
                text = message.caption
                await message.photo[-1].download('test.jpg')
                send(text, 'test.jpg')
            elif message.content_type == 'text':
                text = message.text
                send(text)

    except AttributeError:
        pass

    if message.text is not None:
        logging.info(f'Новое сообщение в канале {message.chat.title}. \n'
                     f'{message.text}')
    elif message.caption is not None:
        logging.info(f'Новое сообщение в канале {message.chat.title}. \n'
                     f'{message.caption}')
