from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from data.config import bot_name
from keyboards.inline.callback_data import like_callback
from loader import dp, bot
from utils.db_api import quick_commands as commands


@dp.callback_query_handler(like_callback.filter(action='up_like'))
async def up_like(call: CallbackQuery):
    await bot.answer_callback_query(call.id, text='Спасибо. Ваш голос учтен.')
    url_comment = call.message.reply_markup["inline_keyboard"][-1][-1]['url']
    message_id = call.message.message_id
    mention_id = str(call.from_user.id)
    # users_str = await commands.get_all_user(post_id=message_id)[0].replace('=', '&').split('&')
    users_str = await commands.get_all_user(post_id=message_id)
    users = users_str.replace('=', '&').split('&')
    if mention_id not in users:
        await commands.update_like(post_id=message_id, user_id=mention_id)
    elif mention_id in users:
        reaction = users[int(users.index(f'{mention_id}')) + 1]
        if reaction == 'like':
            await commands.like_take_away(post_id=message_id)
            # users_old = await commands.get_all_user(post_id=message_id)[0]
            users_old = await commands.get_all_user(post_id=message_id)
            users_new = users_old.replace(f'&{mention_id}=like', '')
            await commands.update_users(post_id=message_id, users=users_new)
        elif reaction == 'ind':
            await commands.indifference_take_away(post_id=message_id)
            # users_old = await commands.get_all_user(post_id=message_id)[0]
            users_old = await commands.get_all_user(post_id=message_id)
            users_new = users_old.replace(f'&{mention_id}=ind', '')
            await commands.update_users(post_id=message_id, users=users_new)
            await commands.update_like(post_id=message_id, user_id=mention_id)
        elif reaction == 'dis':
            await commands.dislike_take_away(post_id=message_id)
            # users_old = await commands.get_all_user(post_id=message_id)[0]
            users_old = await commands.get_all_user(post_id=message_id)
            users_new = users_old.replace(f'&{mention_id}=dis', '')
            await commands.update_users(post_id=message_id, users=users_new)
            await commands.update_like(post_id=message_id, user_id=mention_id)

    like_list = await commands.get_like_condition(post_id=message_id)
    rating_keyboard3 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🔥 {like_list[1]}", callback_data=like_callback.new(action='no_reaction')),
                InlineKeyboardButton(text=f"👍 {like_list[0]}", callback_data=like_callback.new(action='up_like')),
                InlineKeyboardButton(text=f"👎 {like_list[2]}", callback_data=like_callback.new(action='down_like'))
            ],
            [
                InlineKeyboardButton(text='Предложить новость', url=f'http://t.me/{bot_name}?start=start'),
                InlineKeyboardButton(text='Прокомментировать', url=f'{url_comment}'),
            ]
        ]

    )
    await call.message.edit_reply_markup(reply_markup=rating_keyboard3)


@dp.callback_query_handler(like_callback.filter(action='no_reaction'))
async def up_ind(call: CallbackQuery):
    await bot.answer_callback_query(call.id, text='Спасибо. Ваш голос учтен.')
    url_comment = call.message.reply_markup["inline_keyboard"][-1][-1]['url']
    message_id = call.message.message_id
    mention_id = str(call.from_user.id)
    # users = await commands.get_all_user(post_id=message_id)[0].replace('=', '&').split('&')
    users_str = await commands.get_all_user(post_id=message_id)
    users = users_str.replace('=', '&').split('&')
    if mention_id not in users:
        await commands.update_indifference(post_id=message_id, user_id=mention_id)
    elif mention_id in users:
        reaction = users[int(users.index(f'{mention_id}')) + 1]
        if reaction == 'like':
            await commands.like_take_away(post_id=message_id)
            # users_old = await commands.get_all_user(post_id=message_id)[0]
            users_old = await commands.get_all_user(post_id=message_id)
            users_new = users_old.replace(f'&{mention_id}=like', '')
            await commands.update_users(post_id=message_id, users=users_new)
            await commands.update_indifference(post_id=message_id, user_id=mention_id)
        elif reaction == 'ind':
            await commands.indifference_take_away(post_id=message_id)
            # users_old = await commands.get_all_user(post_id=message_id)[0]
            users_old = await commands.get_all_user(post_id=message_id)
            users_new = users_old.replace(f'&{mention_id}=ind', '')
            await commands.update_users(post_id=message_id, users=users_new)

        elif reaction == 'dis':
            await commands.dislike_take_away(post_id=message_id)
            # users_old = await commands.get_all_user(post_id=message_id)[0]
            users_old = await commands.get_all_user(post_id=message_id)
            users_new = users_old.replace(f'&{mention_id}=dis', '')
            await commands.update_users(post_id=message_id, users=users_new)
            await commands.update_indifference(post_id=message_id, user_id=mention_id)

    like_list = await commands.get_like_condition(post_id=message_id)
    rating_keyboard3 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🔥 {like_list[1]}", callback_data=like_callback.new(action='no_reaction')),
                InlineKeyboardButton(text=f"👍 {like_list[0]}", callback_data=like_callback.new(action='up_like')),
                InlineKeyboardButton(text=f"👎 {like_list[2]}", callback_data=like_callback.new(action='down_like'))
            ],
            [
                InlineKeyboardButton(text='Предложить новость', url=f'http://t.me/{bot_name}?start=start'),
                InlineKeyboardButton(text='Прокомментировать', url=f'{url_comment}'),
            ]
        ]

    )
    await call.message.edit_reply_markup(reply_markup=rating_keyboard3)


@dp.callback_query_handler(like_callback.filter(action='down_like'))
async def up_dislike(call: CallbackQuery):
    await bot.answer_callback_query(call.id, text='Спасибо. Ваш голос учтен.')
    url_comment = call.message.reply_markup["inline_keyboard"][-1][-1]['url']
    message_id = call.message.message_id
    mention_id = str(call.from_user.id)
    # users = await commands.get_all_user(post_id=message_id)[0].replace('=', '&').split('&')
    users_str = await commands.get_all_user(post_id=message_id)
    users = users_str.replace('=', '&').split('&')
    if mention_id not in users:
        await commands.update_dislike(post_id=message_id, user_id=mention_id)
    elif mention_id in users:
        reaction = users[int(users.index(f'{mention_id}')) + 1]
        if reaction == 'like':
            await commands.like_take_away(post_id=message_id)
            # users_old = await commands.get_all_user(post_id=message_id)[0]
            users_old = await commands.get_all_user(post_id=message_id)
            users_new = users_old.replace(f'&{mention_id}=like', '')
            await commands.update_users(post_id=message_id, users=users_new)
            await commands.update_dislike(post_id=message_id, user_id=mention_id)
        elif reaction == 'ind':
            await commands.indifference_take_away(post_id=message_id)
            # users_old = await commands.get_all_user(post_id=message_id)[0]
            users_old = await commands.get_all_user(post_id=message_id)
            users_new = users_old.replace(f'&{mention_id}=ind', '')
            await commands.update_users(post_id=message_id, users=users_new)
            await commands.update_dislike(post_id=message_id, user_id=mention_id)
        elif reaction == 'dis':
            await commands.dislike_take_away(post_id=message_id)
            # users_old = await commands.get_all_user(post_id=message_id)[0]
            users_old = await commands.get_all_user(post_id=message_id)
            users_new = users_old.replace(f'&{mention_id}=dis', '')
            await commands.update_users(post_id=message_id, users=users_new)

    like_list = await commands.get_like_condition(post_id=message_id)
    rating_keyboard3 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🔥 {like_list[1]}", callback_data=like_callback.new(action='no_reaction')),
                InlineKeyboardButton(text=f"👍 {like_list[0]}", callback_data=like_callback.new(action='up_like')),
                InlineKeyboardButton(text=f"👎 {like_list[2]}", callback_data=like_callback.new(action='down_like'))
            ],
            [
                InlineKeyboardButton(text='Предложить новость', url=f'http://t.me/{bot_name}?start=start'),
                InlineKeyboardButton(text='Прокомментировать', url=f'{url_comment}'),
            ]
        ]

    )
    await call.message.edit_reply_markup(reply_markup=rating_keyboard3)
