from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, SmallInteger, TIMESTAMP
from datetime import datetime

Base = declarative_base()


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    game_id = Column(String)
    title = Column(String)
    platforms = Column(ARRAY(String))
    base_price = Column(Integer)
    discounted_price = Column(Integer)
    discount = Column(SmallInteger)
    img = Column(String)
    last_modified = Column(TIMESTAMP, default=datetime.now())

    @classmethod
    def table_name(cls, company):
        return f'{company}_games'
