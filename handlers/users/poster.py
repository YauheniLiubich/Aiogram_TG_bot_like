from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.types import CallbackQuery

from keyboards.default import menu
from data.config import admins, channels
from keyboards.inline.manage_post import confirmation_keyborad, post_callback, response_keyboard, \
    send_keyboard, get_post, confirmation_keyborad2

from loader import dp, bot
from utils.db_api import quick_commands as commands
from states.poster import NewPost, CancelPost, MentionId


@dp.message_handler(text='Предложить новость')
@dp.message_handler(CommandStart(deep_link='start'))
@dp.message_handler(Command('create_post'))
async def create_post(message: types.Message):
    await message.answer('Отправьте мне текст поста на публикацию')
    # await message.answer(message)
    await NewPost.EnterMessage.set()


@dp.message_handler(state=NewPost.EnterMessage)
async def enter_message(message: types.Message, state: FSMContext):
    await state.update_data(text=message.html_text,
                            mention=message.from_user.get_mention(),
                            mention_id=message.from_user.id)
    await message.answer('Отправить пост редактору?',
                         reply_markup=confirmation_keyborad2)
    await NewPost.next()


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=NewPost.EnterMessage)
async def enter_message_photo(message: types.Message, state: FSMContext):
    # await message.photo[-1].download()
    await message.reply_photo(message.photo[-1].file_id, caption=message.caption)
    data = {'caption': message.caption,
            'photo_file_id': message.photo[-1].file_id,
            'mention_id': message.from_user.id}

    await state.update_data(data=data, mention=message.from_user.get_mention())

    await message.answer('Отправить пост редактору?',
                         reply_markup=confirmation_keyborad2)
    await NewPost.next()


@dp.callback_query_handler(post_callback.filter(action='post'), state=NewPost.Confirm)
async def confirm_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text = data.get('text')
        caption = data.get('caption')
        photo_file_id = data.get('photo_file_id')
        mention = data.get('mention')
        mention_id = data.get('mention_id')

    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer('Пост отправлен.', reply_markup=menu)

    await bot.send_message(chat_id=admins[0], text='Пришло предложение новости для канала', reply_markup=get_post)
    if text:
        await commands.add_news(user_id=mention_id, content=text, photo_id=None, caption=None, username=mention)
    if photo_file_id:
        await commands.add_news(user_id=mention_id, content=None, photo_id=photo_file_id, caption=caption,
                                username=mention)


@dp.callback_query_handler(post_callback.filter(action='cancel'), state=NewPost.Confirm)
async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer('Вы отклонили пост', reply_markup=menu)


@dp.callback_query_handler(post_callback.filter(action='get_news'), user_id=admins)
async def view_news(call: CallbackQuery, state: FSMContext):
    message = await call.message.edit_reply_markup()
    # print(commands.select_all_news()[-1])
    # news_id, id_user, text, photo_id, caption, username = commands.select_all_news()[-1]
    news_all = await commands.select_all_news()
    news = news_all[-1]
    news_id = news.id
    id_user = news.user_id
    text = news.content
    photo_id = news.photo_id
    caption = news.caption
    username = news.username
    # print(news_id)
    # print(id_user)
    # print(text)
    # print(photo_id)
    # print(caption)
    # print(username)

    await MentionId.EnterMessage.set()
    await state.update_data(news_id=news_id, id_user=id_user)
    await MentionId.next()

    await message.answer(f'Пользователь {username} хочет сделать пост: ')
    if text is not None:
        await message.answer(text=text, reply_markup=confirmation_keyborad)
    if photo_id is not None:
        await message.answer_photo(photo=photo_id, caption=caption, reply_markup=confirmation_keyborad)


@dp.callback_query_handler(post_callback.filter(action='post'), user_id=admins, state=MentionId.Confirm)
async def approve_post(call: CallbackQuery, state: FSMContext):
    await call.answer('Вы одобрили этот пост', show_alert=True)
    target_channel = channels[0]
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=target_channel)
    async with state.proxy() as data:
        news_id = data.get('news_id')
    await commands.delete_news(id=news_id)
    await state.finish()


@dp.callback_query_handler(post_callback.filter(action='cancel'), user_id=admins, state=MentionId.Confirm)
async def decline_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        id_user = data.get('id_user')
        news_id = data.get('news_id')
    await state.finish()
    message = await call.message.edit_reply_markup()
    await message.answer('Укажите причину'
                         , reply_markup=response_keyboard)
    await CancelPost.EnterMessage.set()
    await state.update_data(id_user=id_user, news_id=news_id)


@dp.message_handler(state=CancelPost.EnterMessage, user_id=admins)
async def response_news(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        text = data.get('text')
        id_user = data.get('id_user')
        reply_text_message = data.get('reply_text_message')
        news_id = data.get('news_id')
    await state.update_data(text=message.html_text)
    await message.answer(f'Причина отклонения : \n{message.html_text}', reply_markup=send_keyboard, parse_mode='HTML')
    await CancelPost.next()


@dp.callback_query_handler(post_callback.filter(action='send'), state=CancelPost.Confirm)
async def send_response(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text = data.get('text')
        id_user = data.get('id_user')
        news_id = data.get('news_id')
    answer_text = f'Новость отклонена. \nПричина: {text}'
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer('Вы отправили причину отказа')
    await bot.send_message(chat_id=id_user, text=answer_text, parse_mode='HTML')
    await commands.delete_news(id=news_id)


@dp.callback_query_handler(post_callback.filter(action='non'), user_id=admins, state=CancelPost.EnterMessage)
async def response_cancel(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        news_id = data.get('news_id')
    await commands.delete_news(id=news_id)
    await state.finish()
    await call.message.edit_reply_markup()
    await call.answer('Вы отклонили этот пост', show_alert=True)
