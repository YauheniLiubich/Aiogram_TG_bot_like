from utils.db_api.sqlite import Database

db = Database()


def test():
    # db.create_table_news()
    # # news = db.select_all_news()
    # # print(f'До добавления новостей: {news}')
    # db.add_news(1, 'Текст новости 1')
    # db.add_news(2, None)
    # db.add_news(3, 'Текст новости 3')
    # db.add_news(4, 'Текст новости 4')
    #
    # news = db.select_all_news()
    # print(f'После добавления новостей: {news}')
    #
    # news1 = db.select_one_news(user_id=3)
    # print(f'Получил новость: {news1}')
    # db.delete_news(user_id=3)
    # news = db.select_all_news()
    # print(f'После удаления новостей: {news}')
    try:
        db.create_table_like()
    except:
        pass
    # db.add_post(post_id=1, like=0, indifference=0, dislike=0, user_id='123')
    # db.update_like(post_id=1)
    # db.update_dislike(post_id=1)
    # db.update_indifference(post_id=1)
    db.add_post(post_id=5)
    # db.update_like(post_id=1, user_id='123456789')
    # users = db.get_all_user(post_id=2)[0].split('&')
    # print(users)
    # like_list = db.get_like_condition(post_id=1)
    # print(like_list)
    db.update_users(post_id=1, users='qwerty')
    # db.like_take_away(post_id=1)
    # db.like_take_away(post_id=1)
    # db.like_take_away(post_id=1)
    db.indifference_take_away(post_id=1)
    db.dislike_take_away(post_id=1)
    db.update_like(post_id=1, user_id='7894564123')
    db.update_dislike(post_id=1, user_id='78945dgsdg64123')





test()