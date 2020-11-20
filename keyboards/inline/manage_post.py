from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

post_callback = CallbackData('create_post', 'action')

confirmation_keyborad = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Опубликовать пост', callback_data=post_callback.new(action='post')),
            InlineKeyboardButton(text='Отклонить пост', callback_data=post_callback.new(action='cancel'))
        ]
    ]
)

confirmation_keyborad2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отправить', callback_data=post_callback.new(action='post')),
            InlineKeyboardButton(text='Отменить отправку', callback_data=post_callback.new(action='cancel'))
        ]
    ]
)






response_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Без причины', callback_data=post_callback.new(action='non'))
        ]
    ]
)

send_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Отправить', callback_data=post_callback.new(action='send'))]
    ]
)

get_post = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Посмотреть новость', callback_data=post_callback.new(action='get_news'))]
    ]
)