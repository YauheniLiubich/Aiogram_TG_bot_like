from asyncpg import UniqueViolationError

from utils.db_api.schemas.news import News

from utils.db_api.schemas.like import Like


async def add_news(user_id: int, content: str, photo_id: str, caption: str, username: str):
    try:
        news = News(user_id=user_id, content=content, photo_id=photo_id, caption=caption, username=username)
        await news.create()

    except UniqueViolationError:
        pass


async def select_all_news():
    news = await News.query.gino.all()
    return news


async def select_one_news(post_id):
    news = await News.query.where(News.post_id == post_id).gino.first()
    return news


async def delete_news(id):
    news = await News.get(id)
    await news.delete()


async def add_post(post_id):
    try:
        post = Like(post_id=post_id)
        await post.create()

    except UniqueViolationError:
        pass


async def update_like(post_id: int, user_id: str):
    post = await Like.get(post_id)
    new_count_like = post.like + 1
    new_user_id = post.user_id + f'&{user_id}=like'
    await post.update(like=new_count_like, user_id=new_user_id).apply()


async def like_take_away(post_id):
    post = await Like.get(post_id)
    new_count_like = post.like - 1
    await post.update(like=new_count_like).apply()


async def update_indifference(post_id: int, user_id: str):
    post = await Like.get(post_id)
    new_count_indifference = post.indifference + 1
    new_user_id = post.user_id + f'&{user_id}=ind'
    await post.update(indifference=new_count_indifference, user_id=new_user_id).apply()


async def indifference_take_away(post_id):
    post = await Like.get(post_id)
    new_count_indifference = post.indifference - 1
    await post.update(indifference=new_count_indifference).apply()


async def update_dislike(post_id: int, user_id: str):
    post = await Like.get(post_id)
    new_count_dislike = post.dislike + 1
    new_user_id = post.user_id + f'&{user_id}=dis'
    await post.update(dislike=new_count_dislike, user_id=new_user_id).apply()


async def dislike_take_away(post_id):
    post = await Like.get(post_id)
    new_count_dislike = post.dislike - 1
    await post.update(dislike=new_count_dislike).apply()


async def get_all_user(post_id: int):
    post = await Like.get(post_id)
    all_user = post.user_id
    return all_user


async def get_like_condition(post_id: int):
    post = await Like.get(post_id)
    like = post.like
    indifference = post.indifference
    dislike = post.dislike
    like_condition = (like, indifference, dislike)
    return like_condition


async def update_users(post_id: int, users: str):
    post = await Like.get(post_id)
    await post.update(user_id=users).apply()




