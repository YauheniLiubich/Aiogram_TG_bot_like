from sqlalchemy import Column, BigInteger, Integer, Text, VARCHAR, sql

from utils.db_api.db_gino import TimeBaseModel


class Like(TimeBaseModel):
    __tablename__ = 'Like'
    post_id = Column(BigInteger, primary_key=True)
    like = Column(Integer, default=0)
    indifference= Column(Integer, default=0)
    dislike = Column(Integer, default=0)
    user_id = Column(Text, default='first')

    query: sql.Select