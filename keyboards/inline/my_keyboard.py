from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# like_callback = CallbackData('count_like', 'action')
from keyboards.inline.callback_data import like_callback


rating_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👍", callback_data=like_callback.new(action='up_like')),
            InlineKeyboardButton(text="😐", callback_data=like_callback.new(action='no_reaction')),
            InlineKeyboardButton(text="👎", callback_data=like_callback.new(action='down_like'))
        ],
        [
            InlineKeyboardButton(text='Предложить новость', url='http://t.me/defoldadmin_bot?start=start'),
            InlineKeyboardButton(text='Прокомментировать', callback_data='2'),
        ]
    ]

)

