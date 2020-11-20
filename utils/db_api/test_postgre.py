import asyncio
from utils.db_api.postgresql import Database



async def test():
    await db.create_table_news()
    # await db.add_news(user_id=1, content='Test', photo_id='Test', caption='Test', username='Test')
    # await db.add_news(user_id=2, content='Test', photo_id='Test', caption='Test', username='Test')
    # await db.add_news(user_id=3, content='Test', photo_id='Test', caption='Test', username='Test')
    # await db.add_news(user_id=4, content='Test', photo_id='Test', caption='Test', username='Test')
    # news = await db.select_all_news()
    # print(news[0])
    news = await db.select_one_news(id=2)
    print(news)







loop = asyncio.get_event_loop()
db = Database(loop)

loop.run_until_complete(test())
