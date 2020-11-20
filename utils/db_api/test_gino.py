import asyncio

from data import config
from utils.db_api import quick_commands
from utils.db_api.db_gino import db


async def test():
    await db.set_bind(config.POSTGRES_URI)
    # await db.gino.drop_all()
    await db.gino.create_all()


    print('Добавляем новость')
    # await quick_commands.add_news(
    #     user_id=15,
    #     content='Test',
    #     photo_id='qweasdfx',
    #     caption='test',
    #     username='user'
    # )
    # await quick_commands.add_post(post_id=3)
    # await quick_commands.update_like(post_id=1, user_id='123456')
    # await quick_commands.update_indifference(post_id=1, user_id='123456')
    # await quick_commands.update_dislike(post_id=1, user_id='123456')
    user = await quick_commands.get_all_user(post_id=1)
    # await quick_commands.update_users(post_id=1, users='Новые юзеры')
    # print(user)
    # await quick_commands.like_take_away(post_id=1)
    # await quick_commands.indifference_take_away(post_id=1)
    # await quick_commands.dislike_take_away(post_id=1)
    # lst = await quick_commands.get_like_condition(post_id=1)
    print(user)



    # await quick_commands.like_take_away(post_id=1)

    # await quick_commands.delete_news(2)
    print('Готово')

loop = asyncio.get_event_loop()
loop.run_until_complete(test())