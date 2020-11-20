from sqlalchemy import Column, BigInteger, Integer, Text, VARCHAR, sql

from utils.db_api.db_gino import TimeBaseModel


class News(TimeBaseModel):
    __tablename__ = 'News'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    content = Column(Text)
    photo_id = Column(Text)
    caption = Column(Text)
    username = Column(VARCHAR)

    query: sql.Select
