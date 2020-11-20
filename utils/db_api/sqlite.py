import sqlite3


class Database:
    def __init__(self, path_to_db='news.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False,
                fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()

        connection = self.connection

        # connection.set_trace_callback(logger)

        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        data = None
        if commit:
            connection.commit()

        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()

        return data

    def create_table_news(self):
        sql = """
        CREATE TABLE News (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
        user_id int NOT NULL,
        content TEXT,
        photo_id TEXT,
        caption TEXT,
        username VARCHAR NOT NULL
        );
        """
        self.execute(sql, commit=True)

    def add_news(self, user_id: int, content: str, photo_id: str, caption: str, username: str):
        sql = "INSERT INTO News(user_id, content, photo_id, caption, username) VALUES(?, ?, ?, ?, ?)"
        parameters = (user_id, content, photo_id, caption, username)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_news(self):
        sql = "SELECT * FROM News"
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f'{item}=?' for item in parameters
        ])
        return sql, tuple(parameters.values())

    def select_one_news(self, **kwargs):
        sql = "SELECT * FROM News WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def delete_news(self, **kwargs):
        sql = 'DELETE FROM News WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        self.execute(sql, parameters, commit=True)

    def count_news(self):
        return self.execute("SELECT COUNT(*) FROM News;", fetchone=True)

    def create_table_like(self):
        sql = """
        CREATE TABLE Like (
        post_id int PRIMARY KEY  NOT NULL,
        like int NOT NULL DEFAULT 0,
        indifference int NOT NULL DEFAULT 0,
        dislike int NOT NULL DEFAULT 0,
        user_id TEXT NOT NULL
        );
        """
        self.execute(sql, commit=True)

    def add_post(self, post_id: int):
        sql = "INSERT INTO Like(post_id, like, indifference, dislike, user_id) VALUES(?, 0, 0, 0, 'first')"
        parameters = (post_id,)
        self.execute(sql, parameters=parameters, commit=True)

    def update_like(self, post_id: int, user_id: str):
        sql = f"UPDATE Like SET like=like+1, user_id=user_id||'&{user_id}=like' WHERE post_id={post_id}"
        self.execute(sql, commit=True)

    def like_take_away(self, post_id):
        sql = f"UPDATE Like SET like=like-1 WHERE post_id={post_id}"
        self.execute(sql, commit=True)



    def update_indifference(self, post_id: int, user_id: str):
        sql = f"UPDATE Like SET indifference=indifference+1, user_id=user_id||'&{user_id}=ind'  WHERE post_id={post_id}"
        self.execute(sql, commit=True)

    def indifference_take_away(self, post_id):
        sql = f"UPDATE Like SET indifference=indifference-1 WHERE post_id={post_id}"
        self.execute(sql, commit=True)





    def update_dislike(self, post_id: int, user_id: str):
        sql = f"UPDATE Like SET dislike=dislike+1, user_id=user_id||'&{user_id}=dis'  WHERE post_id={post_id}"
        self.execute(sql, commit=True)

    def dislike_take_away(self, post_id):
        sql = f"UPDATE Like SET dislike=dislike-1 WHERE post_id={post_id}"
        self.execute(sql, commit=True)





    def get_all_user(self, post_id: int):
        sql = f"SELECT user_id FROM Like WHERE post_id={post_id}"
        return self.execute(sql, fetchone=True)





    def get_like_condition(self, post_id: int):
        sql = f"SELECT like, indifference, dislike FROM Like WHERE post_id={post_id}"
        return self.execute(sql, fetchone=True)




    def update_users(self, post_id: int, users: str):
        sql = f"UPDATE Like SET user_id='{users}' WHERE post_id={post_id}"
        self.execute(sql, commit=True)


def logger(statement):
    print(f"""
____________________________________________________
Executing:
{statement}
____________________________________________________
""")
